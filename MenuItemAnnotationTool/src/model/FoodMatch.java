package model;

public class FoodMatch {
	
	private String text;
	private String match;

	public FoodMatch() {
		super();
	}

	public FoodMatch(String text) {
		super();
		this.text = text;
		this.match = null;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public String getMatch() {
		return match;
	}

	public void setMatch(String match) {
		this.match = match;
	}
	
}
