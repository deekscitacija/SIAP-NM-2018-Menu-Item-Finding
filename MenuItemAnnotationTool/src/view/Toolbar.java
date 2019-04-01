package view;

import javax.swing.JButton;
import javax.swing.JToolBar;
import javax.swing.SwingConstants;

import controller.ActionManager;


public class Toolbar extends JToolBar {
	
	private static final long serialVersionUID = 1L;

	public Toolbar() {
		super(SwingConstants.HORIZONTAL);
		setFloatable(false);

		JButton otvori = new JButton(ActionManager.getInstance().getFileChooserDialogContoller());
		add(otvori);
	}

}
