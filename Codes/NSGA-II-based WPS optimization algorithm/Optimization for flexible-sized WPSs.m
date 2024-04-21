
allSolutions = cell(32, 1);
allObjectiveValues = zeros(1, 32);
allYValues = zeros(3, 32);
allTotalObjectives = zeros(1, 32);

for i = 1:32
    LOW = evalin('base', sprintf('LOW%d', i));
    UP  = evalin('base', sprintf('UP%d', i));
    x7 = optimvar("x", 1, 4, "LowerBound", LOW, "UpperBound", UP);
    initialPoint6.x = LOW;
    problem = optimproblem;
    problem.Objective = fcn2optimexpr(@Weight, x7);
    show(problem);
    [solution, objectiveValue, reasonSolverStopped] = solve(problem, initialPoint6, "Solver", "gamultiobj");
    allSolutions{i} = solution.x;
    allObjectiveValues(i) = objectiveValue;
    y1 = TheTotalCost(allSolutions{i});
    y2 = TheAnnualTotalEnergyConsumption(allSolutions{i});
    y3 = TheAnnualUsefulDaylightingIlluminance(allSolutions{i});
    alpha = [0.3, 0.3, 0.4];
    totalObjective = alpha(1) * y1 + alpha(2) * y2 + alpha(3) * y3;
    allYValues(:, i) = [y1; y2; y3];
    allTotalObjectives(i) = totalObjective;
    fprintf("The %d iteration\n", i);
    disp("Decompose vector：");
    disp(allSolutions{i});
    disp("TCO, TEC, UDI：");
    disp(allYValues(:, i));
    disp("Total objective value：");
    disp(allTotalObjectives(i));
    fprintf("\n");
    clearvars x7 initialPoint6 reasonSolverStopped objectiveValue
end
