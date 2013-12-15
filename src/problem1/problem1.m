%{ Author: Stephen Ranshous    %}
%{ Date:   5 December, 2013    %}

% Read the graph file and create the sparse adjacency matrix
filename = '../../datasets/static.network';
g = readGraph(filename);

%% Part (a): Will it spread or die out?
% The effective strength for the SIS model. Beta is the probability of
% transfer, delta is the probability of healing, and C is a constant which
% is based on the model used.
beta = 0.2;
delta = 0.7;
C = beta / delta;
e1 = eigs(g, 1);
ES = C * e1;
fprintf('The effective strength of the virus is %g\n', ES);

if ES >= 1
    fprintf('This value is greater than the threshold so the virus will');
    fprintf(' propagate and spread and kill everyone.\n');
else
    fprintf('This value is below the threshold so everyone will');
    fprintf(' eventually get healthy and the virus will go away.\n');
end

%% Part (b): Hold delta constant, vary beta, plot the value of ES

beta = 0.2;
delta = 0.7;
granularity = 50;
betas = linspace(0, 1, granularity);
ES_varyingBeta = zeros(granularity, 1);

for i = 1:granularity
    beta = betas(i);
    ES = (beta / delta) * e1;
    ES_varyingBeta(i) = ES;
end

figure;
plot(betas, ES_varyingBeta);
title('Varying delta/beta values v1');
xlabel('Value');
ylabel('Effective strength');
legend('Varying beta');
hold on;

%% Part (c): Hold beta constant, vary delta, plot the value of ES

beta = 0.2;
delta = 0.7;
granularity = 50;
deltas = linspace(0, 1, granularity);
ES_varyingBeta = zeros(granularity, 1);

for i = 1:granularity
    delta = deltas(i);
    ES = (beta / delta) * e1;
    ES_varyingBeta(i) = ES;
end

plot(deltas, ES_varyingBeta, '-r');
legend('Varying beta, delta=0.7', 'Varying delta, beta=0.2');
hold off;

%% Part (d): Do (a)-(c) except with different beta and delta values
% The effective strength for the SIS model. Beta is the probability of
% transfer, delta is the probability of healing, and C is a constant which
% is based on the model used.
beta = 0.01;
delta = 0.6;
C = beta / delta;
e1 = eigs(g, 1);
ES = C * e1;
fprintf('The effective strength of the virus is %g\n', ES);

if ES >= 1
    fprintf('This value is greater than the threshold so the virus will');
    fprintf(' propagate and spread and kill everyone.\n');
else
    fprintf('This value is below the threshold so everyone will');
    fprintf(' eventually get healthy and the virus will go away.\n');
end

beta = 0.01;
delta = 0.6;
granularity = 50;
betas = linspace(0, 1, granularity);
ES_varyingBeta = zeros(granularity, 1);

for i = 1:granularity
    beta = betas(i);
    ES = (beta / delta) * e1;
    ES_varyingBeta(i) = ES;
end

figure;
plot(betas, ES_varyingBeta);
title('Varying delta/beta values v2');
xlabel('Value');
ylabel('Effective strength');
legend('Varying beta, delta=0.6');
hold on;

beta = 0.01;
delta = 0.6;
granularity = 50;
deltas = linspace(0, 1, granularity);
ES_varyingBeta = zeros(granularity, 1);

for i = 1:granularity
    delta = deltas(i);
    ES = (beta / delta) * e1;
    ES_varyingBeta(i) = ES;
end

plot(deltas, ES_varyingBeta, '-r');
legend('Varying beta, delta=0.6', 'Varying delta, beta=0.01');