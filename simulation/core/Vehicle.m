classdef Vehicle < handle
    properties
        ID
        Actor
        Behavior
    end
    
    methods
        function obj = Vehicle(id, actor, behavior)
            obj.ID = id;
            obj.Actor = actor;
            obj.Behavior = behavior;
        end
    end
end
