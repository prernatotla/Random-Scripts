function [new_accu, train_accu] = knn_classify(train_data, train_label, new_data, new_label, k)
% k-nearest neighbor classifier
% Input:
%  train_data: N*D matrix, each row as a sample and each column as a
%  feature
%  train_label: N*1 vector, each row as a label
%  new_data: M*D matrix, each row as a sample and each column as a
%  feature
%  new_label: M*1 vector, each row as a label
%  k: number of nearest neighbors
%
% Output:
%  new_accu: accuracy of classifying new_data
%  train_accu: accuracy of classifying train_data (using leave-one-out
%  strategy)
%
% CSCI 576 2014 Fall, Homework 1

training_data_size = size(train_data,1);

accuracy = 0;
% Training accuracy
for i = 1:training_data_size
    test_instance = train_data(i,:);
    top_k(1:k,2) = Inf;
    for j = 1:training_data_size
        if j == i
            continue
        end
        % L2 norm
        distance = norm(test_instance - train_data(j,:));
        class = train_label(j);
        temp1_d = distance;
        temp1_c = class;
        for t = 1:k
            if top_k(t,2) > temp1_d
                temp2_c = top_k(t,1);
                temp2_d = top_k(t,2);
                top_k(t,:) = [temp1_c,temp1_d];
                temp1_c = temp2_c;
                temp1_d = temp2_d;
            end
        end
    end
    % Majority Vote
    unique_classes = unique(top_k(:,1));
    majority_vote_class = -1;
    majority_vote_size = 0;
    for label = unique_classes'
        % Naive voting
        class_size = size(find(top_k(:,1) == label),1);
        if class_size > majority_vote_size
            majority_vote_class = label;
            majority_vote_size = class_size;
        end
    end
    if majority_vote_class == train_label(i)
        accuracy = accuracy + 1;
    end
end
train_accu = accuracy/training_data_size

accuracy = 0;
new_data_size = size(new_data,1);
% Training accuracy
for i = 1:new_data_size
    test_instance = new_data(i,:);
    % k rows - [class, distance]
    top_k(1:k,2) = Inf;
    for j = 1:training_data_size
        % L2 norm
        distance = norm(test_instance - train_data(j,:));
        class = train_label(j);
        temp1_d = distance;
        temp1_c = class;
        for t = 1:k
            if top_k(t,2) > temp1_d
                temp2_c = top_k(t,1);
                temp2_d = top_k(t,2);
                top_k(t,:) = [temp1_c,temp1_d];
                temp1_c = temp2_c;
                temp1_d = temp2_d;
            end
        end
    end
    % Majority Vote
    unique_classes = unique(top_k(:,1));
    majority_vote_class = -1;
    majority_vote_size = 0;
    for label = unique_classes'
        class_size = size(find(top_k(:,1) == label),1);
        if class_size > majority_vote_size
            majority_vote_class = label;
            majority_vote_size = class_size;
        end
    end
    if majority_vote_class == new_label(i)
        accuracy = accuracy + 1;
    end
end

new_accu = accuracy / new_data_size

