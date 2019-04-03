package controller;

import java.awt.event.ActionEvent;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import javax.swing.AbstractAction;
import javax.swing.ImageIcon;
import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;

import org.apache.commons.io.FilenameUtils;
import org.json.simple.parser.ParseException;

import model.Restaurant;
import model.ReviewMatch;
import utils.JsonParseUtil;
import utils.MessageUtils;
import view.MainFrame;
import view.MatchingPanel;
import view.MenuItemDisplay;

public class MultipleFileChooserDialogController extends AbstractAction{
	
	private static final long serialVersionUID = 1L;

	public MultipleFileChooserDialogController() {
		putValue(AbstractAction.NAME, "Otvorite fajl");
		putValue(AbstractAction.SHORT_DESCRIPTION, "Otvorite fajl");
		putValue(AbstractAction.SMALL_ICON, new ImageIcon("resources/icons/file.png"));
	}

	@Override
	public void actionPerformed(ActionEvent arg0) {
		
		MainFrame mf = MainFrame.getInstance();
		
		JFileChooser chooser = new JFileChooser();
		chooser.setDialogTitle("Izaberite fajl");
		chooser.setMultiSelectionEnabled(true);
		chooser.setFileFilter(new FileNameExtensionFilter("*.json", "json"));
	    
	    if(!mf.getDirectoryPath().isEmpty()) {
	    	chooser.setCurrentDirectory(new File(mf.getDirectoryPath()));
	    }
	    
	    if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
	    	File[] selectedFiles = chooser.getSelectedFiles();
	    	ArrayList<String> tempFiles = new ArrayList<String>();
	    	
	    	//Add paths to all .json files from directory to list
	    	for (File file : selectedFiles) {
			    if (file.isFile()) {
			    	tempFiles.add(file.getAbsolutePath());
			    }
			}
	    	
	    	//Save as properties to MainFrame for easier access
			mf.setDirectoryPath(selectedFiles[0].getParent());
			mf.setFileNames(tempFiles);
			
			//Deserialize first revew file
			ReviewMatch reviewMatch = deserializeReview(mf.getFileNames());
			
			if(reviewMatch == null) {
				MessageUtils.showNullErrorMessage();
				return;
			}
			
			Restaurant restaurant = mf.getMongoRepository().getRestaurant(reviewMatch.getRestaurantLink());
			mf.switchView(new MenuItemDisplay(reviewMatch, reviewMatch.getMenuItems().get(0), restaurant.getRestaurantName(), 0, 0), new MatchingPanel(restaurant));
	    }
		
	}
	
	private ReviewMatch deserializeReview(ArrayList<String> tempFiles) {
		
		ReviewMatch retVal  = null;
		try {
			if(!tempFiles.isEmpty()) {
				retVal = JsonParseUtil.parseReviewMatch(tempFiles.get(0));
				if(retVal.getMenuItems().isEmpty()) {
					MessageUtils.showEmptyFoodMatches(retVal.getId());
					tempFiles.remove(0);
					return deserializeReview(tempFiles);
				}	
			}
		} catch (IOException | ParseException e1) {
			MessageUtils.showParseErrorMessage(tempFiles.get(0));
			return null;
		}
		
		return retVal;
	}

}
