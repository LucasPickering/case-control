package me.lucaspickering.casecontrol.command.lcd;

import java.awt.*;

import me.lucaspickering.casecontrol.CaseControl;
import me.lucaspickering.casecontrol.Data;
import me.lucaspickering.casecontrol.Funcs;
import me.lucaspickering.casecontrol.command.AbstractCommand;

public final class CommandLcdColor extends AbstractCommand {

  @Override
  public String getName() {
    return "color";
  }

  @Override
  public String getArgDesc() {
    return "<color>";
  }

  @Override
  public String getFullDesc() {
    return "Sets the color of the LCD.";
  }

  @Override
  public boolean execute(String[] args) {
    Color color;
    if (args.length >= 1 && (color = Funcs.getColor(args[0])) != null) {
      Data data = CaseControl.getData();
      data.lcdStaticColor = color; // Set the static color
      // TODO: Set LCD mode to clock if it is currently off
      return true;
    } else {
      return false;
    }
  }
}
