Authors:
	Micaela Vieira, Nadja Näf

Steps:
1. Create a txt file with the inputs for the eye tracker experiment (Data/input_data.txt);
2. Use generate_lists.py to divide the inputs into several files according to a Latin square design;
3. Create a yaml file to store information for the eye tracker experiment (iohub_config.yaml);
4. Use eye_tracker_experiment.py to perform the experiment;
5. The output of the experiment is a hdf5 file (events.hdf5);  <-- TO CHECK AND UPDATE
6. Read the hdf5 file with the hdfView software <-- TO IMPLEMENT

Note:
- the eye_tracker_experiment.py script is based on the psychophysics GitHub (https://github.com/psychopy/psychopy/tree/release/psychopy/demos/coder/iohub) and on chapter 19 of J. Peirce & M. MacaAkill - Building Experiments in Psychopy (retrievable at https://1lib.ch/book/11813584/6fb110).


###########################################
                  TO DO
###########################################
- check yaml file for correctness
- add pauses with recalibration
- add drift corrections
- add multiple monitors
- store values and info about the trial into the hdf5 file
- read hdf5 to see if the procedure is correct
- other???
- finish presentation (work in progress, first version coming soon)
