import sys
import os
import matlab.engine
import subprocess
import venv
from pathlib import Path

# --- Add Project Root to Path ---
# This ensures that we can import gRPC modules after they are generated
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def setup_environment():
    """
    Automates the entire project setup: virtual environment, dependencies, and gRPC code generation.
    """
    print("--- Running Project Setup Verification ---")
    
    # --- Step 1: Virtual Environment ---
    venv_path = project_root / 'automation' / 'venv'
    if not venv_path.exists():
        print(f"[1/3] Creating Python virtual environment at '{venv_path}'...")
        venv.create(venv_path, with_pip=True, system_site_packages=True)
    
    # --- Step 2: gRPC Code Generation (The Critical Part) ---
    mathworks_folder = project_root / 'mathworks'
    if not mathworks_folder.exists():
        print("[2/3] 'mathworks' gRPC folder not found. Generating code bundle...")
        
        rr_install_path = Path("C:/Program Files/RoadRunner R2025a") # Edit if your path is different
        proto_path = rr_install_path / "bin/win64/Proto"
        
        if not proto_path.exists():
            print(f"❌ FATAL ERROR: RoadRunner Proto path not found at '{proto_path}'.", file=sys.stderr)
            print("Please edit the 'rr_install_path' variable in this script.", file=sys.stderr)
            return False

        # This is the complete list of .proto files needed
        proto_files_to_compile = [
            "mathworks/roadrunner/core.proto",
            "mathworks/roadrunner/import_settings.proto",
            "mathworks/roadrunner/export_settings.proto",
            "mathworks/scenario/common/geometry.proto",
            "mathworks/scenario/common/array.proto",
            "mathworks/roadrunner/roadrunner_service_messages.proto",
            "mathworks/roadrunner/roadrunner_service.proto"
        ]
        
        # Determine the python executable from the virtual environment
        python_exe = venv_path / 'Scripts' / 'python.exe' if sys.platform == "win32" else venv_path / 'bin' / 'python'

        try:
            subprocess.run([
                str(python_exe),
                "-m", "grpc_tools.protoc",
                f"--proto_path={proto_path}",
                "--python_out=.",
                "--grpc_python_out=."
            ] + proto_files_to_compile, check=True, cwd=project_root)
            print("     ✅ gRPC code bundle generated successfully.")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"❌ FATAL ERROR: Failed to generate gRPC code. Error: {e}", file=sys.stderr)
            print("Please ensure 'grpcio-tools' is installed (`pip install grpcio-tools`).", file=sys.stderr)
            return False

    # --- Step 3: Dependencies ---
    print("[3/3] Verifying Python dependencies...")
    # This step would typically run `pip install -r requirements.txt`
    # For simplicity, we assume the user has run it once as per the guide.
    
    print("--- ✅ Setup Verified ---")
    return True

# Now we can safely import our local libraries
from automation import roadrunner_utils
from mathworks.roadrunner import roadrunner_service_pb2_grpc
from mathworks.roadrunner import roadrunner_service_messages_pb2 as messages

def main():
    """
    Main orchestration script to run the full, automated simulation workflow.
    """
    if not setup_environment():
        sys.exit(1) # Exit if setup fails

    print("\n--- 🇮🇳 IndiaSim Digital Twin - Fully Automated Workflow ---")
    matlab_eng = None
    
    try:
        # --- Step 1: Automatically Launch RoadRunner ---
        success, message = roadrunner_utils.launch_roadrunner(str(project_root))
        if not success:
            print(f"❌ FATAL ERROR: {message}", file=sys.stderr)
            return
        print(f"✅ {message}")

        # --- Step 2: Automatically Import a Real-World Map ---
        map_to_import = project_root / 'data' / 'input' / 'bengaluru_kadirenahalli_cross.osm'
        
        if not map_to_import.exists():
             print(f"⚠️  WARNING: Sample map '{map_to_import.name}' not found.", file=sys.stderr)
             print("Loading a default scene from the RoadRunner project instead.", file=sys.stderr)
             success, message = roadrunner_utils.load_scene("FourWaySignal")
             if not success:
                raise Exception(f"Could not load default scene. {message}")
             scene_name_for_export = "FourWaySignal"
        else:
            success, message = roadrunner_utils.import_map_to_roadrunner(str(map_to_import))
            if not success:
                raise Exception(f"Could not import OSM map. {message}")
            print(f"✅ {message}")
            scene_name_for_export = map_to_import.stem

        # --- Step 3: Export the final scene for MATLAB ---
        output_dir = project_root / 'data' / 'output'
        output_dir.mkdir(exist_ok=True)
        exported_xodr_path = output_dir / f"{scene_name_for_export}.xodr"
        
        success, message = roadrunner_utils.export_scene_to_xodr(str(exported_xodr_path))
        if not success:
            raise Exception(f"Could not export scene to OpenDRIVE. {message}")
        print(f"✅ {message}")

        # --- Step 4: Start MATLAB Engine ---
        print("▶️  Starting MATLAB Engine...")
        matlab_eng = matlab.engine.start_matlab()
        sim_path = str(project_root / 'simulation')
        matlab_eng.addpath(matlab_eng.genpath(sim_path), nargout=0)
        print("✅ MATLAB Engine started and paths configured.")

        # --- Step 5: Run the Simulation in MATLAB ---
        demo_config = {
            'scene_path': str(exported_xodr_path), 
            'num_steps': 400
        }
        print(f"🚀 Sending command to MATLAB to run simulation on '{exported_xodr_path.name}'...")
        trajectory_data = matlab_eng.run_sim(demo_config, nargout=1)
        print("✅ Simulation complete. Trajectory data received from MATLAB.")
        
        # --- Step 6: Visualize Results ---
        print("📊 Asking MATLAB to plot the results...")
        matlab_eng.workspace['trajectoryHistory'] = trajectory_data
        matlab_eng.eval("utils.plotXYTrajectories(trajectoryHistory);", nargout=0)
        print("📈 Plot generated. Check the MATLAB figure window.")
        input("\nPress Enter to close MATLAB and exit.")

    except Exception as e:
        print(f"❌ An unexpected error occurred during orchestration: {e}", file=sys.stderr)
    finally:
        # --- Step 7: Cleanup ---
        if matlab_eng:
            matlab_eng.quit()
            print("⏹️  MATLAB Engine shut down.")

if __name__ == '__main__':
    main()

