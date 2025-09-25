function plotXYTrajectories(trajectoryHistory)
    % Plots the X-Y paths of all vehicles from the simulation output.
    figure;
    ax = axes;
    hold(ax, 'on');
    grid(ax, 'on');
    colors = lines(numel(trajectoryHistory));
    
    for i = 1:numel(trajectoryHistory)
        trajectory = trajectoryHistory{i};
        plot(ax, trajectory(:,1), trajectory(:,2), 'LineWidth', 2, 'Color', colors(i,:));
    end
    
    hold(ax, 'off');
    title('Vehicle XY Trajectories');
    xlabel('X (m)');
    ylabel('Y (m)');
    axis equal;
    legend(ax, {'Car', 'Weaving Bike'});
end
