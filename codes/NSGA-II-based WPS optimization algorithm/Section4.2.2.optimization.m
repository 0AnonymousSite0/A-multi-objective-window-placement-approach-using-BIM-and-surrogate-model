allSolutions = cell(32, 1);
allObjectiveValues = zeros(1, 32);

for i = 1:32

    LOW = evalin('base', sprintf('LOW%d', i));
    UP  = evalin('base', sprintf('UP%d', i));
    problem = optimproblem;
    x7 = optimvar("x", 1, 4, "LowerBound", LOW, "UpperBound", UP);
    cons1 = x7(1) - x7(3) == 3;
    cons2 = x7(2) - x7(4) == 1.5;

    problem.Constraints.cons1 = cons1;
    problem.Constraints.cons2 = cons2;

    initialPoint6.x = UP;
    problem.Objective = fcn2optimexpr(@Weight, x7);
    show(problem);
    [solution, objectiveValue, reasonSolverStopped] = solve(problem, initialPoint6, "Solver", "gamultiobj");

    allSolutions{i} = solution.x;
    allObjectiveValues(i) = objectiveValue;

    solution
    reasonSolverStopped
    objectiveValue

    clearvars x7 initialPoint6 reasonSolverStopped objectiveValue
end


for i = 1:4:32
    fprintf("The %d-%d iteration\n", i, min(i+3, 32)); 
    disp("Decompose vector：");

    for j = i:min(i+3, 32)
        solution = allSolutions{j}; 
        vertex = solution(1:2);
        diagonal = solution(3:4);
        
        fprintf("Iteration %d：\n", j);
        fprintf("Vertex coordinates：[%f, %f]\n", vertex(1), vertex(2));
        fprintf("Diagonal coordinates：[%f, %f]\n", diagonal(1), diagonal(2));
        

        y = Weight(solution);
        a = TheTotalCost(solution);
        b = TheAnnualTotalEnergyConsumption(solution);
        c = TheAnnualUsefulDaylightingIlluminance(solution);
        
        fprintf("The function value of a：%f\n", a);
        fprintf("The function value of b：%f\n", b);
        fprintf("The function value of c：%f\n", c);
        fprintf("\n");
    end
end

results = zeros(32, 1);
for i = 1:32

    x = eval(['LOW', num2str(i)]);
 
    z = myWeightedFunctiontotalNEW1127(x);

    results(i) = z;

    y = Weight(allSolutions{j});
    a = TheTotalCost(allSolutions{j});
    b = TheAnnualTotalEnergyConsumption(allSolutions{j});
    c = TheAnnualUsefulDaylightingIlluminance(allSolutions{j});
        
    fprintf("The function value of a：%f\n", a);
    fprintf("The function value of b：%f\n", b);
    fprintf("The function value of c：%f\n", c);
    fprintf("\n");
end

resultsTable = table((1:32)', results, 'VariableNames', {'Index', 'ZValue'});
disp(resultsTable);
writetable(resultsTable, 'results.xlsx');

