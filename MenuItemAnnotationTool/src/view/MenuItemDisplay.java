package view;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.util.ArrayList;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.border.EmptyBorder;

import model.FoodMatch;
import model.ReviewMatch;

public class MenuItemDisplay extends JPanel{
	
	private static final long serialVersionUID = 1L;

	private ReviewMatch reviewMatch = null;
	private FoodMatch foodMatch = null;
	private ArrayList<FoodMatch> totalMatches = new ArrayList<FoodMatch>();
	private String restaurantName = "None";
	private int reviewCount = 0;
	private int foodCount = 0;

	public MenuItemDisplay() {
		initialize();
	}
	
	public MenuItemDisplay(ReviewMatch reviewMatch, FoodMatch foodMatch, String restaurantName, int reviewCount, int foodCount) {
		super();
		this.reviewMatch = reviewMatch;
		this.foodMatch = foodMatch;
		this.restaurantName = restaurantName;
		this.reviewCount = reviewCount;
		this.foodCount = foodCount;
		this.totalMatches = new ArrayList<>();
		initialize();
	}

	private void initialize() {
		setLayout(new BorderLayout());
		setBorder(new EmptyBorder(30, 30, 30, 30));
		
		JLabel titleLabel1 = new JLabel("Review: "+(reviewMatch == null ? "None" : reviewMatch.getId()));
		titleLabel1.setFont(new Font(titleLabel1.getName(), Font.PLAIN, 22));
		titleLabel1.setForeground(new Color(50, 50, 50));
		
		JLabel titleLabel2 = new JLabel("Restoran: "+restaurantName);
		titleLabel2.setFont(new Font(titleLabel2.getName(), Font.PLAIN, 22));
		titleLabel2.setForeground(new Color(50, 50, 50));
		
		JLabel titleLabel3 = new JLabel("Obradjeno review-a: "+reviewCount);
		titleLabel3.setFont(new Font(titleLabel3.getName(), Font.PLAIN, 22));
		titleLabel3.setForeground(new Color(50, 50, 50));
		
		JLabel titleLabel4 = new JLabel("Obradjeno stavki hrane: "+foodCount);
		titleLabel4.setFont(new Font(titleLabel3.getName(), Font.PLAIN, 22));
		titleLabel4.setForeground(new Color(50, 50, 50));
		
		JLabel titleLabel5 = new JLabel("Naziv pronadjene hrane: ");
		titleLabel5.setFont(new Font(titleLabel4.getName(), Font.PLAIN, 22));
		titleLabel5.setForeground(new Color(50, 50, 50));
		
		JTextArea foodNameLabel = new JTextArea(1, 1);
		foodNameLabel.setText(foodMatch == null ? "None" : foodMatch.getText());
		foodNameLabel.setFont(new Font(titleLabel1.getName(), Font.ITALIC, 26));
		foodNameLabel.setMaximumSize(new Dimension(400, 300));
		foodNameLabel.setBackground(new Color(255, 255, 179));
		foodNameLabel.setEditable(false);
		
		JPanel labelPanel = new JPanel();
		labelPanel.setLayout(new BoxLayout(labelPanel, BoxLayout.PAGE_AXIS));
		labelPanel.setBackground(Color.WHITE);
		
		labelPanel.add(titleLabel1);
		labelPanel.add(Box.createRigidArea(new Dimension(0,5)));
		labelPanel.add(titleLabel2);
		labelPanel.add(Box.createRigidArea(new Dimension(0,5)));
		labelPanel.add(titleLabel3);
		labelPanel.add(Box.createRigidArea(new Dimension(0,5)));
		labelPanel.add(titleLabel4);
		labelPanel.add(Box.createRigidArea(new Dimension(0,30)));
		labelPanel.add(titleLabel5);
		labelPanel.add(Box.createRigidArea(new Dimension(0,10)));
		
		JPanel contentPanel = new JPanel(new BorderLayout());
		contentPanel.add(labelPanel, BorderLayout.NORTH);
		contentPanel.add(foodNameLabel, BorderLayout.CENTER);
		
		setBackground(Color.WHITE);
		add(contentPanel, BorderLayout.CENTER);
	}
	
	public MenuItemDisplay switchReview(ReviewMatch reviewMatch, String restaurantName) {
		this.reviewMatch = reviewMatch;
		this.foodMatch = reviewMatch.getMenuItems().get(0);
		this.restaurantName = restaurantName;
		this.foodCount++;
		this.reviewCount++;
		this.totalMatches = new ArrayList<>();
		removeAll();
		initialize();
		return this;
	}
	
	public MenuItemDisplay switchFoodMatch() {
		this.foodMatch = reviewMatch.getMenuItems().get(0);
		this.foodCount++;
		removeAll();
		initialize();
		return this;
	}

	public ReviewMatch getReviewMatch() {
		return reviewMatch;
	}

	public void setReviewMatch(ReviewMatch reviewMatch) {
		this.reviewMatch = reviewMatch;
	}

	public FoodMatch getFoodMatch() {
		return foodMatch;
	}

	public void setFoodMatch(FoodMatch foodMatch) {
		this.foodMatch = foodMatch;
		repaint();
	}

	public String getRestaurantName() {
		return restaurantName;
	}

	public void setRestaurantName(String restaurantName) {
		this.restaurantName = restaurantName;
	}

	public int getReviewCount() {
		return reviewCount;
	}

	public void setReviewCount(int reviewCount) {
		this.reviewCount = reviewCount;
	}

	public ArrayList<FoodMatch> getTotalMatches() {
		return totalMatches;
	}

	public void setTotalMatches(ArrayList<FoodMatch> totalMatches) {
		this.totalMatches = totalMatches;
	}

	public int getFoodCount() {
		return foodCount;
	}

	public void setFoodCount(int foodCount) {
		this.foodCount = foodCount;
	}
	
}
