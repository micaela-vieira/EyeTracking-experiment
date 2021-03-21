Project for the course "21FS 521d505a Eye tracking: From experiment design to statistical and machine learning-based data analysis".

THE PROCESSING OF SUBJECT AND OBJECT RELATIVE CLAUSES IN GERMAN


Author:
	Micaela Vieira

Steps:
1. Create a txt file with the inputs for the eye tracker experiment (Data/input_data.txt);
2. Use generate_lists.py to divide the inputs into several files according to a Latin square design;
3. Create a yaml file to store information for the eye tracker experiment (iohub_config.yaml);
4. Use eye_tracker_experiment.py to perform the experiment;
5. The output of the experiment is a hdf5 file (events.hdf5);
6. Read the hdf5 file with check_output_content.py.

Note:
- the eye_tracker_experiment.py script is based on the psychophysics GitHub (https://github.com/psychopy/psychopy/tree/release/psychopy/demos/coder/iohub) and on chapter 19 of J. Peirce & M. MacaAkill - Building Experiments in Psychopy (retrievable at https://1lib.ch/book/11813584/6fb110).


###########################################
                  TO DO
###########################################
- add pauses selected by user and experimenter
- add drift corrections
- add multiple monitors
- other???
- finish presentation (work in progress, first version coming soon)
