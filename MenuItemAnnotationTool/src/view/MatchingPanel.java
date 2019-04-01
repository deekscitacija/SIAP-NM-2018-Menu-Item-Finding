package view;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.border.EmptyBorder;

import controller.ActionManager;
import model.MenuItem;
import model.Restaurant;

public class MatchingPanel extends JPanel{
	
	private static final long serialVersionUID = 1L;
	
	private Restaurant restaurant = null;
	private JList<Object> listView = null;
	
	public MatchingPanel() {
		initialize();
	}
	
	public MatchingPanel(Restaurant restaurant) {
		this.restaurant = restaurant;
		initialize();
	}
	
	public void initialize(){
		
		setLayout(new BorderLayout());
		setBorder(new EmptyBorder(30, 70, 30, 70));
		
		JLabel titleLabel1 = new JLabel("Slaze se sa: ");
		titleLabel1.setFont(new Font(titleLabel1.getName(), Font.PLAIN, 22));
		titleLabel1.setForeground(new Color(50, 50, 50));
		
		ArrayList<MenuItem> items = new ArrayList<MenuItem>();
		items.add(new MenuItem("None", "No description"));
		if(restaurant != null) {
			items.addAll(restaurant.getMenuItems());
		}
		
		listView = new JList<Object>(items.toArray()); 
		listView.setCellRenderer(new MenuItemCellRenderer());
		listView.setSelectedIndex(0);
		JScrollPane listScroller = new JScrollPane(listView);
		listScroller.setBorder(new EmptyBorder(20, 0, 20, 0));
		
		JButton submit = new JButton(ActionManager.getInstance().getSubmitController());
		submit.setOpaque(true);
		submit.setBackground(new Color(255, 153, 51));
		submit.setFont(new Font(titleLabel1.getName(), Font.PLAIN, 18));
		submit.setPreferredSize(new Dimension(50, 50));
		
		add(titleLabel1, BorderLayout.NORTH);
		add(submit, BorderLayout.SOUTH);
		add(listScroller);
	}
	
	public MenuItem getSelectedMenuItem() {
		
		int selectedIdx = listView.getSelectedIndex();
		
		if(selectedIdx != -1) {
			return (MenuItem) listView.getSelectedValue();
		}
		
		return null;
	}

	public Restaurant getRestaurant() {
		return restaurant;
	}

	public void setRestaurant(Restaurant restaurant) {
		this.restaurant = restaurant;
	}

}
