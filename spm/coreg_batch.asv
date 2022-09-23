%------------------------------------------------------------------------
% Batch script for registering a set of nifti images using the SPM batch
% system. The SPM functions used are 'spm_coreg' and 'spm_reslice'.
% For more information about this functions check the following links:
%   (1)https://github.com/neurodebian/spm12/blob/master/spm_coreg.m
%   (2)https://github.com/neurodebian/spm12/blob/master/spm_reslice.m
%------------------------------------------------------------------------

clear;clc;
%>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
%PARAMETERS
%<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

% prefix for the file name of the registered niftis
coregPrefix = 'r_';

%>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
%MAIN SCRIPT
%<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

% select the niftis to register
[path_subs,n_subs] = select_elements([1 Inf],'nii','Select images to coregister','',1);

% select reference niftis
% if only one is selected, this is going to be used for every subject
[path_refs,n_refs] = select_elements([1 n_subs],'nii','Select reference images','',1);
if n_refs ~= 1 && n_refs ~= n_subs
    error('[ERROR] When more than one reference image is selected, the amoun8t of references needs to be equal to the images to coregister');
end

% load the coregister module for the batch
load('coregister_module.mat');

% batch configuration
matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.prefix = coregPrefix;

myBatch = cell(1,n_subs);
for s = 1:n_subs
    fprintf("\n[INFO] %s",path_subs(s,:));
    %[folder,fname,ext] = fileparts(path_subs(s,:));
    myBatch{s} = matlabbatch{1};
    myBatch{s}.spm.spatial.coreg.estwrite.source = {path_subs(s,:)};
    
    % if only one ref was selected, this images is going to be used as
    % reference for every subject. If more than one ref is selected means
    % that there was selected a corresponding reference for every subject
    if n_refs > 1
        path_ref = path_refs(s,:);
    elseif n_refs == 1
        path_ref = path_refs(1,:);
    end
    myBatch{s}.spm.spatial.coreg.estwrite.ref = {path_ref};
end

%run the spm batch
fprintf('\n[INFO] Coregistering...\n');
spm_jobman('run',myBatch);
fprintf('[INFO]Job Done!\n');