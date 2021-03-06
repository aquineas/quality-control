
class QCConfig():
    " configuration options for how to run checks "

    def __init__(self, 
        enable_experimental = False,
        results_dir = "results",
        images_dir = "images", 
        save_results = False,
        plot_models = False,
        ):

        # checks
        self.results_dir = results_dir
        self.save_results = save_results
        self.enable_experimental = enable_experimental

        # forecast
        self.images_dir = images_dir
        self.plot_models = plot_models
