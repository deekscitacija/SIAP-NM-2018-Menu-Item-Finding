package utils;

import javax.swing.JDialog;
import javax.swing.JOptionPane;

public class MessageUtils {

	public static void showParseErrorMessage(String path) {
		JOptionPane optionPane = new JOptionPane("Greska prilikom parsiranja .json fajle sa recenzijom na putanji : \n"+path, JOptionPane.ERROR_MESSAGE);    
		JDialog dialog = optionPane.createDialog("Greska prilikom parsiranja");
		dialog.setAlwaysOnTop(true);
		dialog.setVisible(true);
	}
	
	public static void showNullErrorMessage() {
		JOptionPane optionPane = new JOptionPane("Sadraj review-a koji ucitali iz .json datoteke nije validan.", JOptionPane.ERROR_MESSAGE);    
		JDialog dialog = optionPane.createDialog("Validacija");
		dialog.setAlwaysOnTop(true);
		dialog.setVisible(true);
	}
	
	public static void showEmptyFolderErrorMessage(String path) {
		JOptionPane optionPane = new JOptionPane("Izabrani folder na putanji : "+path+"\n ne sadrzi ni jednu .json datoteku pogodnu za anotiranje.", JOptionPane.ERROR_MESSAGE);    
		JDialog dialog = optionPane.createDialog("Nema datoteka za obradu");
		dialog.setAlwaysOnTop(true);
		dialog.setVisible(true);
	}
	
	public static void showEmptyListErrorMessage(String path) {
		JOptionPane optionPane = new JOptionPane("Izabrani review na putanji : "+path+"\n ne sadrzi ni jednu pronadjenu stavku menija.", JOptionPane.ERROR_MESSAGE);    
		JDialog dialog = optionPane.createDialog("Nema pronadjenih stavki menija");
		dialog.setAlwaysOnTop(true);
		dialog.setVisible(true);
	}
	
	public static void showFinishedFolderParsing(String path) {
		JOptionPane optionPane = new JOptionPane("Uspesno ste labelisali sve review-w sa putanje : "+path+".\n Mozete ucitati naredni direktorijum.", JOptionPane.INFORMATION_MESSAGE);    
		JDialog dialog = optionPane.createDialog("Uspesno labelisanje");
		dialog.setAlwaysOnTop(true);
		dialog.setVisible(true);
	}
	
	public static void showSerializationErrorMessage() {
		JOptionPane optionPane = new JOptionPane("Greska prilikom cuvanja review-a u .json datoteku.", JOptionPane.ERROR_MESSAGE);    
		JDialog dialog = optionPane.createDialog("Serijalizacija");
		dialog.setAlwaysOnTop(true);
		dialog.setVisible(true);
	}
}
