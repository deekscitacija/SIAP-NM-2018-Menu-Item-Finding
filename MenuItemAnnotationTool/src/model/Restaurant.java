package model;

import java.util.ArrayList;

public class Restaurant {
	
	private String restaurantLink;
	private String restaurantName; 
	private String restaurantCountry;
	private String restaurantCity;
	private ArrayList<MenuItem> menuItems;
	
	public Restaurant() {
		super();
	}
	
	public Restaurant(String restaurantLink, String restaurantName, String restaurantCountry, String restaurantCity,
			ArrayList<MenuItem> menuItems) {
		super();
		this.restaurantLink = restaurantLink;
		this.restaurantName = restaurantName;
		this.restaurantCountry = restaurantCountry;
		this.restaurantCity = restaurantCity;
		this.menuItems = menuItems;
	}

	public String getRestaurantLink() {
		return restaurantLink;
	}

	public void setRestaurantLink(String restaurantLink) {
		this.restaurantLink = restaurantLink;
	}

	public String getRestaurantName() {
		return restaurantName;
	}

	public void setRestaurantName(String restaurantName) {
		this.restaurantName = restaurantName;
	}

	public String getRestaurantCountry() {
		return restaurantCountry;
	}

	public void setRestaurantCountry(String restaurantCountry) {
		this.restaurantCountry = restaurantCountry;
	}

	public String getRestaurantCity() {
		return restaurantCity;
	}

	public void setRestaurantCity(String restaurantCity) {
		this.restaurantCity = restaurantCity;
	}

	public ArrayList<MenuItem> getMenuItems() {
		return menuItems;
	}

	public void setMenuItems(ArrayList<MenuItem> menuItems) {
		this.menuItems = menuItems;
	}
	
}
