package model;

import java.util.ArrayList;

public class ReviewMatch {
	
	private String id;
	
	private String restaurantLink;
	
	private ArrayList<FoodMatch> menuItems;

	public ReviewMatch() {
		super();
	}

	public ReviewMatch(String id, String restaurantLink, ArrayList<FoodMatch> menuItems) {
		super();
		this.id = id;
		this.restaurantLink = restaurantLink;
		this.menuItems = menuItems;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getRestaurantLink() {
		return restaurantLink;
	}

	public void setRestaurantLink(String restaurantLink) {
		this.restaurantLink = restaurantLink;
	}

	public ArrayList<FoodMatch> getMenuItems() {
		return menuItems;
	}

	public void setMenuItems(ArrayList<FoodMatch> menuItems) {
		this.menuItems = menuItems;
	}

	@Override
	public String toString() {
		String retVal = "ReviewMatch [id=" + id + ", restaurantLink=" + restaurantLink + ", foodMatches= ";
		
		if(menuItems != null) {
			for(FoodMatch aMatch : menuItems) {
				retVal+=aMatch.getText()+", ";
			}
		}
		
		return retVal+"]";
	}
	
	

}
