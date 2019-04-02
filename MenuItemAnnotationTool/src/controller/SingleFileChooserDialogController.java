package controller;

import java.awt.event.ActionEvent;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import javax.swing.AbstractAction;
import javax.swing.ImageIcon;
import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;

import org.json.simple.parser.ParseException;

import model.Restaurant;
import model.ReviewMatch;
import utils.JsonParseUtil;
import utils.MessageUtils;
import view.MainFrame;
import view.MatchingPanel;
import view.MenuItemDisplay;

public class SingleFileChooserDialogController extends AbstractAction{
	
	private static final long serialVersionUID = 1L;

	public SingleFileChooserDialogController() {
		putValue(AbstractAction.NAME, "Otvorite fajl");
		putValue(AbstractAction.SHORT_DESCRIPTION, "Otvorite fajl");
		putValue(AbstractAction.SMALL_ICON, new ImageIcon("resources/icons/file.png"));
	}

	@Override
	public void actionPerformed(ActionEvent arg0) {
		
		MainFrame mf = MainFrame.getInstance();
		
		JFileChooser chooser = new JFileChooser();
		chooser.setDialogTitle("Izaberite fajl");
		chooser.setFileFilter(new FileNameExtensionFilter("*.json", "json"));
	    
	    if(!mf.getDirectoryPath().isEmpty()) {
	    	chooser.setCurrentDirectory(new File(mf.getDirectoryPath()));
	    }
	    
	    if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
	    	File selectedFile = chooser.getSelectedFile();
	    	String filePath = selectedFile.getAbsolutePath();
	    	String directoryPath = selectedFile.getParent();
	    	
	    	//Add single file path
	    	ArrayList<String> tempFiles = new ArrayList<String>();
	    	tempFiles.add(filePath);
	    	
	    	//Save as properties to MainFrame for easier access
			mf.setDirectoryPath(directoryPath);
			mf.setFileNames(tempFiles);
			
			//Deserialize first revew file
			ReviewMatch reviewMatch;
			
			try {
				reviewMatch = JsonParseUtil.parseReviewMatch(filePath);
			} catch (IOException | ParseException e1) {
				MessageUtils.showParseErrorMessage(filePath);
				return;
			}
			
			if(reviewMatch == null) {
				MessageUtils.showNullErrorMessage();
				return;
			}
			
			Restaurant restaurant = mf.getMongoRepository().getRestaurant(reviewMatch.getRestaurantLink());
			mf.switchView(new MenuItemDisplay(reviewMatch, reviewMatch.getMenuItems().get(0), restaurant.getRestaurantName(), 0, 0), new MatchingPanel(restaurant));
	    	
	    }
		
	}

}
