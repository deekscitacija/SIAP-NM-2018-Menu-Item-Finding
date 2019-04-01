package view;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Toolkit;
import java.util.ArrayList;

import javax.swing.JFrame;

import db.MongoRepository;

public class MainFrame extends JFrame {
	
	private static final long serialVersionUID = 1L;

	private static MainFrame instance = null;
	
	private MongoRepository mongoRepository = null;
	private MenuItemDisplay menuItemDisplay = null;
	private MatchingPanel matchingPanel = null;
	private Toolbar toolbar = null;
	
	private String directoryPath = "";
	private ArrayList<String> fileNames = new ArrayList<String>();

	private MainFrame() {
		initializeView();
	}
	
	public static MainFrame getInstance() {
		if (instance == null) {
			instance = new MainFrame();
		}
		return instance;
	}
	
	private void initializeView() {
		setTitle("Menu Items Annotation Tool");
		setLayout(new BorderLayout());
		Toolkit kit = Toolkit.getDefaultToolkit();
		Dimension dimenzijeEkrana = kit.getScreenSize();
		int height = dimenzijeEkrana.height;
		int width = dimenzijeEkrana.width;

		setSize(6 * width / 7 , 6 * height / 7);

		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setLocationRelativeTo(null);
		
		toolbar = new Toolbar();
		toolbar.setPreferredSize(new Dimension(0, 70));
		toolbar.setMinimumSize(new Dimension(this.getSize()));
		toolbar.setBackground(new Color(255, 255, 179));
		add(toolbar, BorderLayout.NORTH);
		
		menuItemDisplay = new MenuItemDisplay();
		menuItemDisplay.setPreferredSize(new Dimension(getWidth() / 2, getHeight()));
		add(menuItemDisplay, BorderLayout.WEST);
		
		matchingPanel = new MatchingPanel();
		matchingPanel.setPreferredSize(new Dimension(getWidth() / 2, getHeight()));
		add(matchingPanel, BorderLayout.EAST);
		
		mongoRepository = new MongoRepository();
		
	}
	
	public void switchMenuItemDisplay(MenuItemDisplay newMenuItemDisplay) {
		remove(menuItemDisplay);
		menuItemDisplay = newMenuItemDisplay;
		menuItemDisplay.setPreferredSize(new Dimension(getWidth() / 2, getHeight()));
		add(menuItemDisplay, BorderLayout.WEST);
		revalidate();
		repaint();
	}
	
	public void switchView(MenuItemDisplay newMenuItemDisplay, MatchingPanel newMatchingPanel) {
		remove(menuItemDisplay);
		remove(matchingPanel);
		menuItemDisplay = newMenuItemDisplay;
		matchingPanel = newMatchingPanel;
		menuItemDisplay.setPreferredSize(new Dimension(getWidth() / 2, getHeight()));
		matchingPanel.setPreferredSize(new Dimension(getWidth() / 2, getHeight()));
		add(menuItemDisplay, BorderLayout.WEST);
		add(matchingPanel, BorderLayout.EAST);
		revalidate();
		repaint();
	}

	public ArrayList<String> getFileNames() {
		return fileNames;
	}

	public void setFileNames(ArrayList<String> fileNames) {
		this.fileNames = fileNames;
	}

	public String getDirectoryPath() {
		return directoryPath;
	}

	public void setDirectoryPath(String directoryPath) {
		this.directoryPath = directoryPath;
	}

	public MongoRepository getMongoRepository() {
		return mongoRepository;
	}

	public MenuItemDisplay getMenuItemDisplay() {
		return menuItemDisplay;
	}

	public MatchingPanel getMatchingPanel() {
		return matchingPanel;
	}

	public Toolbar getToolbar() {
		return toolbar;
	}

}
