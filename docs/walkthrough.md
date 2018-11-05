# Brown CBC's RefChef Sample Workflow / Walkthrough

Now, we will provide a brief worked example of how to operate this software.  Please download the files located at the following links, depending on your platform:

Both of these sets of files accomplish the exact same tasks; they contain small differences in the method of generating md5 files and deleting intermediary files.

### Sample Files

To begin, please download and extract the following zip file; a manifest of its contents is as follows:

master_test.yaml - a sample "Master" YAML file for testing

new_test.yaml - a sample "New" YAML file for testing

new_norun_test.yaml - another sample "New" YAML file for further testing

end_result.yaml - a YAML that is (almost) identical to the results of running this tutorial to validate that your implementation has succeeded


### Walkthrough

Some very minor editing of these YAML files is necessary before running the software.  Please open both master_test.yaml and new_test.yaml and edit their 'root-directory' lines to a location on your computer; this directory will be where the references are deposited.  This step is why end_result.yaml is 'almost' identical to what your end result will be, as we cannot predict your local file structure.

*NB: One of the commands used in these YAMLs, 'md5', is Mac-specific.  The corresponding command on most Linux systems is 'md5sum', so running this walkthrough to completion on Linux requires those commands be changed as well*.

From there, we can run the software in both its useful modes.  We will begin by running with only a Master YAML, and then continue by running with both a Master YAML and a New YAML to add additional references.

To initiate a reference download according to the Master YAML's specifications, type::

	python newparser.py local --master master_test.yaml --execute

It will take approximately 30 minutes for this task to complete (depending heavily on your own network's capabilities).  Once it is done, you can check in the directory you designated as 'root-directory' to verify that the files have been obtained.  You should see two subfolders, "ucsc-hg19-concatenate" and "ucsc-hg38", each with a multitude of files.

Now that we have some references, we have created a situation in which we can expand our inventory thereof.  This tool exists to maintain an up-to-date master list of references on the system, and running it with the New YAML will demonstrate this capability by updating the Master YAML::

	python newparser.py local --master master_test.yaml --new new_test.yaml --execute

This reference is rather large, and will likely take another 30 minutes unto itself.  Once it is complete, you can verify two things that have now transpired: first, there is a new subfolder in 'root-directory' entitled "hg38", and second, new_test.yaml's 'reference-entries' has been appended to master_test.yaml and thus master_test.yaml now has the corresponding "hg38" subentry.

Finally, we will run the tool one more time with both a Master YAML, our embiggened master_test.yaml, and the other New YAML, new_norun_test.yaml.  As implied by the name, we will not instruct parseyaml to run new_norun_test.yaml; oftentimes, a user will be creating their YAMLs retrospectively after the manual download of a new reference to serve as a permanent record of their actions, so this set of options will just append the New YAML without actually downloading anything::

	python newparser.py --master master_test.yaml --new new_norun_test.yaml

Note that 'root-directory' does not contain a new subdirectory called "mm9", even though that entry has been appended to master_test.yaml.

Running the software without excecution ensures that new references are added to the Master YAML with the correct sequential number and line formatting, mitigating the possibility of human error in copying and pasting.

With these three commands run, master_test.yaml should now be identical to end_result.yaml aside from the file path specified in 'root-directory'.  These sample files can be edited to get a sense of how options like 'retrieve' work, and will provide a syntactical skeleton for adding further references as the user sees fit.