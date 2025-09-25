classdef TrafficSimulator < handle
    properties
        RoadNetwork
        Vehicles % Cell array of core.Vehicle objects
    end
    
    methods
        function obj = TrafficSimulator(roadNetwork)
            obj.RoadNetwork = roadNetwork;
            obj.Vehicles = {};
        end
        
        function addVehicle(obj, vehicle)
            obj.Vehicles{end+1} = vehicle;
        end

        function step(obj)
            % This is where more complex, non-path-based logic will go in the future
            advance(obj.RoadNetwork.Scenario);
        end
    end
end
s