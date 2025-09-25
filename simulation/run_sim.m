function trajectoryData = run_sim(config)
    % This is the main MATLAB function called by the Python orchestrator.
    % It is designed to be a general interface for running simulations.
    
    disp('--- MATLAB: Received command from Python. Initializing simulation. ---');
    
    % 1. Create a scenario and load the road network from the file provided by Python
    scenario = drivingScenario;
    % Use the 'core' package for the RoadNetwork class
    road_network = core.RoadNetwork(scenario, config.scene_path);
    disp(['--- MATLAB: Loaded scene: ', config.scene_path, ' ---']);

    % 2. Add Actors with Custom Behaviors
    % This demonstrates the "Simulate weaving bikes" objective.
    car = vehicle(scenario, 'ClassID', 1, 'Position', [-40, -2, 0]);
    path(car, [-40, -2, 0; 80, -2, 0], 15); % Straight path
    
    % Generate a custom weaving path using the 'utils' package
    bike_path = utils.generateWeavingPath([-30, 2, 0], [70, 2, 0]);
    bike = vehicle(scenario, 'ClassID', 5, 'Position', bike_path(1,:));
    path(bike, bike_path, 20); % Follows the custom weaving path
    disp('--- MATLAB: Added vehicles with custom paths. ---');
    
    % 3. Run the main simulation loop
    disp('--- MATLAB: Starting simulation loop... ---');
    numSteps = config.num_steps;
    trajectoryHistory = cell(1, numel(scenario.Actors));
    for step = 1:numSteps
        advance(scenario);
        poses = actorPoses(scenario);
        for v_idx = 1:numel(poses)
            trajectoryHistory{v_idx}(step, :) = poses(v_idx).Position;
        end
    end
    
    disp('--- MATLAB: Simulation finished. Returning data to Python. ---');
    trajectoryData = trajectoryHistory;
end
