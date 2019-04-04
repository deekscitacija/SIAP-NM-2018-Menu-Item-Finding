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
		
		String retVal = "";
		boolean matchFound = false;
		
		for(char c : value.toCharArray()) {
			if(c == 'Č' || c == 'Ć') {
				retVal+='C';
				continue;
			}else if(c == 'č' || c == 'ć') {
				retVal+='c';
				continue;
			}else if(c == 'Š') {
				retVal+='S';
				continue;
			}else if(c == 'š') {
				retVal+='s';
				continue;
			}else if(c == 'Ž') {
				retVal+='Z';
				continue;
			}else if(c == 'ž') {
				retVal+='z';
				continue;
			}else if(c == 'Đ') {
				retVal+="Dj";
				continue;
			}else if(c == 'đ') {
				retVal+="dj";
				continue;
			}else {
				retVal+=c;
			}
		}
		
		do{
			matchFound = false;
			if(retVal.length() > 9) {
				if(retVal.substring(retVal.length() - 9).toLowerCase().equals("popularno")) {
					retVal = retVal.substring(0, retVal.length() - 9);
					matchFound = true;
				}
			}
			
			if(retVal.length() > 5) {
				if(retVal.substring(retVal.length() - 5).toLowerCase().equals("posno") || retVal.substring(retVal.length() - 5).toLowerCase().equals("ljuto")) {
					retVal = retVal.substring(0, retVal.length() - 5);
					matchFound = true;
				}
			}
			
			if(retVal.length() > 4) {
				if(retVal.substring(retVal.length() - 4).toLowerCase().equals("novo")) {
					retVal = retVal.substring(0, retVal.length() - 4);
					matchFound = true;
				}
			}
			
			retVal = retVal.trim();
			
		}while(matchFound);
		
		return retVal;
	}
	
}
