package controller;

import java.awt.event.ActionEvent;
import java.io.IOException;
import java.util.ArrayList;

import javax.swing.AbstractAction;
import javax.swing.ImageIcon;

import org.json.simple.parser.ParseException;

import com.google.gson.JsonIOException;

import model.FoodMatch;
import model.Restaurant;
import model.ReviewMatch;
import utils.JsonParseUtil;
import utils.MessageUtils;
import view.MainFrame;
import view.MatchingPanel;

public class SubmitController extends AbstractAction {
	
	private static final long serialVersionUID = 1L;

	public SubmitController() {
		putValue(AbstractAction.NAME, "Potvrdi");
		putValue(AbstractAction.SHORT_DESCRIPTION, "Potvrdi");
		putValue(AbstractAction.SMALL_ICON, new ImageIcon("resources/icons/save.png"));
	}

	@Override
	public void actionPerformed(ActionEvent arg0) {
		MainFrame mf = MainFrame.getInstance();
		
		ArrayList<FoodMatch> remainingFood = mf.getMenuItemDisplay().getReviewMatch().getMenuItems();
		ArrayList<String> remainingPaths = mf.getFileNames();
		
		//If both empty, nothing to do here...
		if(remainingFood.isEmpty() && remainingPaths.isEmpty()) {
			MessageUtils.showEmptyFolderErrorMessage(mf.getDirectoryPath());
			return;
		}
		
		//Merge food mention with its match
		FoodMatch item = remainingFood.get(0);
		item.setMatch(mf.getMatchingPanel().getSelectedMenuItem().getName());
		mf.getMenuItemDisplay().getTotalMatches().add(item);
		
		//Food item is processed, remove it
		remainingFood.remove(0);
		
		//Has any food left unprocessed in this review?
		if(remainingFood.isEmpty()) {
			
			//Food list is empty, save review with its matched food mentions to .json file, get next review
			remainingPaths.remove(0);
			
			ReviewMatch toSave = mf.getMenuItemDisplay().getReviewMatch();
			toSave.setMenuItems(mf.getMenuItemDisplay().getTotalMatches());
			
			try {
				JsonParseUtil.saveReview(toSave, mf.getDirectoryPath());
			} catch (JsonIOException | IOException e) {
				MessageUtils.showSerializationErrorMessage();
				return;
			}
			
			//No more reviews to process? Directory is successfully annotated  
			if(remainingPaths.isEmpty()) {
				MessageUtils.showFinishedFolderParsing(mf.getDirectoryPath());
				return;
			}else {
				//More reviews to process, get next review 
				ReviewMatch reviewMatch;
				try {
					reviewMatch = JsonParseUtil.parseReviewMatch(remainingPaths.get(0));
				} catch (IOException | ParseException e) {
					MessageUtils.showParseErrorMessage(mf.getDirectoryPath());
					return;
				}
				
				if(reviewMatch == null) {
					MessageUtils.showNullErrorMessage();
					return;
				}
				
				//Get restaurant from BD, update view
				Restaurant restaurant = mf.getMongoRepository().getRestaurant(reviewMatch.getRestaurantLink());
				mf.switchView(mf.getMenuItemDisplay().switchReview(reviewMatch, restaurant.getRestaurantName()), new MatchingPanel(restaurant));
			}
		}else {
			//More food in this review, get next food mention
			mf.switchMenuItemDisplay(mf.getMenuItemDisplay().switchFoodMatch());
		}
	}

}
