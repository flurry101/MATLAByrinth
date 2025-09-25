classdef RoadNetwork < handle
    properties
        Scenario
    end
    
    methods
        function obj = RoadNetwork(scenario, openDrivePath)
            obj.Scenario = scenario;
            roadNetwork(obj.Scenario, 'OpenDRIVE', openDrivePath);
        end
    end
end
