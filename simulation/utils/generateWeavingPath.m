function path = generateWeavingPath(startPoint, endPoint)
    % Generates a weaving path for a vehicle.
    % This simulates an erratic driving behavior common in Indian traffic.
    
    % Define the straight line path
    lineVec = endPoint - startPoint;
    numPoints = 50;
    path = zeros(numPoints, 3);
    for i = 1:numPoints
        path(i, :) = startPoint + (i-1)/(numPoints-1) * lineVec;
    end
    
    % Add sinusoidal weaving motion perpendicular to the path
    perpendicularVec = [-lineVec(2), lineVec(1), 0]; % 90-degree rotation
    perpendicularVec = perpendicularVec / norm(perpendicularVec); % Normalize
    
    amplitude = 1.5; % Weave 1.5 meters side-to-side
    frequency = 4;   % Complete 4 weave cycles over the path
    
    for i = 1:numPoints
        progress = (i-1) / (numPoints-1);
        weaveOffset = amplitude * sin(progress * frequency * 2 * pi);
        path(i, :) = path(i, :) + weaveOffset * perpendicularVec;
    end
end

