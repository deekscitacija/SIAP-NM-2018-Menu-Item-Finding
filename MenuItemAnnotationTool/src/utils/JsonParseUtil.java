package utils;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.google.gson.Gson;
import com.google.gson.JsonIOException;

import model.ReviewMatch;

public class JsonParseUtil {
	
	public static Gson gson = new Gson();
	public static JSONParser parser = new JSONParser();

	public static ReviewMatch parseReviewMatch(String path) throws FileNotFoundException, IOException, ParseException {
		
		JSONObject reviewMatch = null;
		reviewMatch = (JSONObject) parser.parse(new FileReader(path));
		return gson.fromJson(reviewMatch.toString(), ReviewMatch.class);
	}
	
	public static void saveReview(ReviewMatch review, String path) throws JsonIOException, IOException {
		FileWriter writer = new FileWriter(path+File.separator+review.getId()+"_match.json");
		gson.toJson(review, writer);
		writer.flush();
		writer.close();
	}
	
	public static String removeLatinCharacters(String value) {
		
		return null;
	}
	
}
