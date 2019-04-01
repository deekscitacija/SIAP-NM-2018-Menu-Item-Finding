package view;

import java.awt.Color;
import java.awt.Component;
import java.awt.Font;

import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.ListCellRenderer;

import model.MenuItem;

public class MenuItemCellRenderer extends JLabel implements ListCellRenderer<Object>  {

	private static final long serialVersionUID = 1L;
	
	public MenuItemCellRenderer() {
		setOpaque(true);
		setIconTextGap(5);
	}

	@Override
	public Component getListCellRendererComponent(JList<?> list, Object value, int index, boolean isSelected, boolean cellHasFocus) {
		
		MenuItem menuItem = (MenuItem) value;
		setText(menuItem.getName());
		setFont(new Font(list.getName(), Font.PLAIN, 22));
		if (isSelected) {
		      setBackground(new Color(153, 255, 204));
		    } else {
		      setBackground(Color.WHITE);
		      setForeground(Color.BLACK);
		}
		return this;
	}

}
