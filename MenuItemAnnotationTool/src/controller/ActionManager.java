package controller;


public class ActionManager {
	
	private static ActionManager instance = null;
	
	private FileChooserDialogContoller fileChooserDialogContoller = null;
	private SingleFileChooserDialogController singleFileChooserDialogContoller = null;
	private SubmitController submitController = null;
	
	private ActionManager() {
		initializeActions();
	}

	public static ActionManager getInstance() {
		
		if (instance == null) {
			instance = new ActionManager();
		}
		return instance;
	}

	private void initializeActions() {
		this.fileChooserDialogContoller = new FileChooserDialogContoller();
		this.submitController = new SubmitController();
		this.singleFileChooserDialogContoller = new SingleFileChooserDialogController();
	}

	public FileChooserDialogContoller getFileChooserDialogContoller() {
		return fileChooserDialogContoller;
	}

	public void setFileChooserDialogContoller(FileChooserDialogContoller fileChooserDialogContoller) {
		this.fileChooserDialogContoller = fileChooserDialogContoller;
	}

	public SubmitController getSubmitController() {
		return submitController;
	}

	public void setSubmitController(SubmitController submitController) {
		this.submitController = submitController;
	}

	public SingleFileChooserDialogController getSingleFileChooserDialogContoller() {
		return singleFileChooserDialogContoller;
	}

	public void setSingleFileChooserDialogContoller(SingleFileChooserDialogController singleFileChooserDialogContoller) {
		this.singleFileChooserDialogContoller = singleFileChooserDialogContoller;
	}
	
}
