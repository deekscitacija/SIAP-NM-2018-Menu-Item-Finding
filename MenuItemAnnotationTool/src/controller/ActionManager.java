package controller;


public class ActionManager {
	
	private static ActionManager instance = null;
	
	private FileChooserDialogContoller fileChooserDialogContoller = null;
	private MultipleFileChooserDialogController multipleFileChooserDialogController = null;
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
		this.multipleFileChooserDialogController = new MultipleFileChooserDialogController();
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

	public MultipleFileChooserDialogController getMultipleFileChooserDialogController() {
		return multipleFileChooserDialogController;
	}

	public void setMultipleFileChooserDialogController(
			MultipleFileChooserDialogController multipleFileChooserDialogController) {
		this.multipleFileChooserDialogController = multipleFileChooserDialogController;
	}
	
}
