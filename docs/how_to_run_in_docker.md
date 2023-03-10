# How to Run the Everactive ENV+ EvalKit Exploration Notebook in Docker

We've created a Dockerized version of the notebook that can be run locally on your machine. This methodology has been tested on MacOS, running Docker Desktop, and using Chrome to interact with JupyterLab.

## Instructions

1. Clone the [notebook repo](https://github.com/everactive/python-notebook-sample) to your local machine:
   ```
   git clone https://github.com/everactive/python-notebook-sample.git
   ```

1. Open a terminal and navigate to the root directory of the cloned repo.

1. Run `./build.sh` to build the Docker container. The Docker build may take several minutes to complete.

1. Once the Docker image is built, run `./run.sh` to start the container. The run script will automate setup of the Docker container and JupyterLab server for you, and will expose the notebook so that you can interact with it via a local web browser on your computer.

   Note that you can supply your [Everactive API credentials](https://support.everactive.com/hc/en-us/articles/6279483691159-Creating-Your-First-API-Credential) when invoking the run script (as opposed to providing the credentials in the notebook itself). To do so, include the `EVERACTIVE_CLIENT_ID` and `EVERACTIVE_CLIENT_SECRET` environment variables in the script invocation command:

   ```
   EVERACTIVE_CLIENT_ID=xxxxxxx EVERACTIVE_CLIENT_SECRET=xxxxxxx ./run.sh
   ```

1. When the script pauses after starting JupyterLab within Docker, you'll see the following output in the terminal:

   ![Run script waiting for user prompt](images/docker/run_script_waiting_for_termination.png)

1. Copy and paste the full localhost URL into your web browser of choice. In the example above, you would use the following URL:<br>`http://127.0.0.1:8888/lab?token=e29f27bfc09d20126bc7256b6a2dec4bbfc093c4079554fc`

   Note that the JupyterLab URL token will change each time you rerun the Docker container.

1. Double click on the notebook name in the left-hand file browser menu to open it.

   ![Open notebook from Jupyter file browser menu](images/docker/open_notebook_from_file_browser.png)

1. If you receive a dialog box prompting you to select a kernel, select the `everactive-envplus` kernel.

   ![Select the everactive-envplus kernel](images/docker/select_a_kernel.png)

1. At this point, you are ready to run the notebook. Go forth and explore!

   ![Ready to run notebook](images/docker/ready_to_use_notebook.png)

1. When you are done, close the web browser and return to the run script in the terminal. Press `Enter` to shut down the Docker container.

   ![Terminated run script](images/docker/run_script_terminated.png)
