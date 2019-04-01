package db;

import java.util.ArrayList;

import org.bson.Document;

import com.mongodb.BasicDBObject;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

import model.MenuItem;
import model.Restaurant;

public class MongoRepository {
	
	private MongoClient mongoClient;
	private MongoDatabase db;

	public MongoRepository() {
		MongoClientURI uri = new MongoClientURI("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net/test?retryWrites=true");
		mongoClient = new MongoClient(uri);
		db = mongoClient.getDatabase("RestaurantData");
	}
	
	@SuppressWarnings("unchecked")
	public Restaurant getRestaurant(String restaurantLink) {
		MongoCollection<Document> collection = db.getCollection("Restaurants");
		BasicDBObject query = new BasicDBObject("restaurantLink", restaurantLink);
		Document restaurantDocument = collection.find(query).first();
		
		Restaurant retVal = new Restaurant();
		retVal.setRestaurantLink(restaurantLink);
		retVal.setRestaurantCountry(restaurantDocument.getString("restaurantCountry"));
		retVal.setRestaurantCity(restaurantDocument.getString("restaurantCity"));
		retVal.setRestaurantName(restaurantDocument.getString("restaurantName"));
		retVal.setMenuItems(new ArrayList<MenuItem>());
		
		ArrayList<Document> menuItemDocuments = restaurantDocument.get("menuItems", ArrayList.class);
		
		for(Document menuItemInfo : menuItemDocuments) {
			MenuItem tempItem = new MenuItem(menuItemInfo.getString("name"), menuItemInfo.getString("description"));
			retVal.getMenuItems().add(tempItem);
		}
		
		return retVal;
	}
}
