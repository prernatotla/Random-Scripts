function [new_accu, train_accu] = naive_bayes(train_data, train_label, new_data, new_label)
% naive bayes classifier
% Input:
%  train_data: N*D matrix, each row as a sample and each column as a
%  feature
%  train_label: N*1 vector, each row as a label
%  new_data: M*D matrix, each row as a sample and each column as a
%  feature
%  new_label: M*1 vector, each row as a label
%
% Output:label
%  new_accu: accuracy of classifying new_data
%  train_accu: accuracy of classifying train_data 
%
% CSCI 576 2014 Fall, Homework 1

% D*1 vector of feature frequencies
% feature_frequencies = sum(train_data);

training_data_size = size(train_data,1);

unique_labels = unique(train_label)';
num_unique_labels = size(unique_labels,2);
probabilities = zeros(num_unique_labels,1); % num_unique_labels unique labels, probability of each
log_feature_probability = zeros(num_unique_labels,21); % num_unique_labels unique labels, probability of each feature given that label
complement_log_feature_probability = zeros(num_unique_labels,21);

% Calculate feature probabilities
% Take log probabilities to prevent underflow
for i = 1:num_unique_labels
    label = unique_labels(i);
    indices = find(train_label == label)';
    label_data = train_data(indices,:);
    label_size = size(label_data,1);
    label_probability = label_size / training_data_size;
    probabilities(i,1) = label_probability;
    label_frequencies = sum(label_data);
    % Add-1 smoothing
    % label_frequencies = label_frequencies + 1;
    feature_probabilities = label_frequencies / (label_size);
    % Constant smoothing
    for j = 1:size(feature_probabilities,2)
        if feature_probabilities(j) == 1
            feature_probabilities(j) = 0.99;
        end
        if feature_probabilities(j) == 0
            feature_probabilities(j) = 0.01;
        end
    end
    log_feature_probability(i,:) = log(feature_probabilities);
    complement_log_feature_probability(i,:) = log(1-feature_probabilities);
end

accuracy = 0;
for i = 1:training_data_size
    instance = train_data(i,:);
    instance_complement = abs(1-instance);
    % Max arg of log_probability (since denominator is P(X) and can be removed from comparison)
    % P(X1 | A) . P(X2 | A) .... P(A) (for each A i.e. each label)
    log_probability_vector = log(probabilities);
    for j = 1:num_unique_labels
        %log_probability_vector = log(probabilities)
        instance_prob = instance .* log_feature_probability(j,:);
        instance_complement_prob = instance_complement .* complement_log_feature_probability(j,:);
        log_probability_vector(j) = log_probability_vector(j) + sum(instance_prob) + sum(instance_complement_prob);
    end
    label = find(log_probability_vector == max(log_probability_vector));
    if train_label(i) == label
        accuracy = accuracy + 1;
    end
end

train_accu = accuracy/training_data_size

new_data_size = size(new_data,1);
accuracy = 0;
for i = 1:new_data_size
    instance = new_data(i,:);
    instance_complement = abs(1-instance);
    % Max arg of log_probability (since denominator is P(X) and can be removed from comparison)
    % P(X1 | A) . P(X2 | A) .... P(A) (for each A i.e. each label)
    log_probability_vector = log(probabilities);
    for j = 1:num_unique_labels
        instance_prob = instance .* log_feature_probability(j,:);
        instance_complement_prob = instance_complement .* complement_log_feature_probability(j,:);
        log_probability_vector(j) = log_probability_vector(j) + sum(instance_prob) + sum(instance_complement_prob);
    end
    label = find(log_probability_vector == max(log_probability_vector));
    if new_label(i) == label
        accuracy = accuracy + 1;
    end
end

new_accu = accuracy/new_data_size


