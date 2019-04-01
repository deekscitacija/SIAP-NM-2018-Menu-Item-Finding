package controller;

import java.awt.event.ActionEvent;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import javax.swing.AbstractAction;
import javax.swing.ImageIcon;
import javax.swing.JFileChooser;

import org.apache.commons.io.FilenameUtils;
import org.json.simple.parser.ParseException;

import model.Restaurant;
import model.ReviewMatch;
import utils.JsonParseUtil;
import utils.MessageUtils;
import view.MainFrame;
import view.MatchingPanel;
import view.MenuItemDisplay;

public class FileChooserDialogContoller extends AbstractAction{
	
	private static final long serialVersionUID = 1L;

	public FileChooserDialogContoller() {
		putValue(AbstractAction.NAME, "Otvorite folder");
		putValue(AbstractAction.SHORT_DESCRIPTION, "Otvorite folder");
		putValue(AbstractAction.SMALL_ICON, new ImageIcon("resources/icons/upload.png"));
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		
		MainFrame mf = MainFrame.getInstance();
		
		JFileChooser chooser = new JFileChooser();
		chooser.setDialogTitle("Izaberite direktorijum");
	    chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
	    
	    if(!mf.getDirectoryPath().isEmpty()) {
	    	chooser.setCurrentDirectory(new File(mf.getDirectoryPath()));
	    }
	    
		if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
			String directoryPath = chooser.getSelectedFile().getAbsolutePath();
			ArrayList<String> tempFiles = new ArrayList<String>();
			
			File folder = new File(directoryPath);
			File[] listOfFiles = folder.listFiles();

			//Add paths to all .json files from directory to list
			for (File file : listOfFiles) {
			    if (file.isFile()) {
			    	if(FilenameUtils.getExtension(file.getAbsolutePath()).equals("json")) {
			    		tempFiles.add(file.getAbsolutePath());
			    	}
			    }
			}
			
			if(tempFiles.isEmpty()) {
				MessageUtils.showEmptyFolderErrorMessage(directoryPath);
				return;
			}
			
			//Save as properties to MainFrame for easier access
			mf.setDirectoryPath(directoryPath);
			mf.setFileNames(tempFiles);
			
			//Deserialize first revew file
			ReviewMatch reviewMatch;
			
			try {
				reviewMatch = JsonParseUtil.parseReviewMatch(tempFiles.get(0));
			} catch (IOException | ParseException e1) {
				MessageUtils.showParseErrorMessage(tempFiles.get(0));
				return;
			}
			
			if(reviewMatch == null) {
				MessageUtils.showNullErrorMessage();
				return;
			}
			
			//Get restaurant from BD, update view
			Restaurant restaurant = mf.getMongoRepository().getRestaurant(reviewMatch.getRestaurantLink());
			mf.switchView(new MenuItemDisplay(reviewMatch, reviewMatch.getMenuItems().get(0), restaurant.getRestaurantName(), 0, 0), new MatchingPanel(restaurant));
		}
		
	}

}
