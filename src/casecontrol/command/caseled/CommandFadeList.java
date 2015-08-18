package casecontrol.command.caseled;

import java.awt.Color;

import casecontrol.Data;
import casecontrol.command.Command;

public final class CommandFadeList implements Command {
  @Override
  public String getName() {
    return "fadelist";
  }

  @Override
  public int getArgumentAmount() {
    return 0;
  }

  @Override
  public String getArgs() {
    return "";
  }

  @Override
  public String getDesc() {
    return "List the current case fade colors.";
  }

  @Override
  public boolean execute(String[] args) {
    for (int i = 0; i < Data.caseFadeColors.size(); i++) {
      Color color = Data.caseFadeColors.get(i);
      System.out.printf("%d - (%d, %d, %d)\n", i, color.getRed(), color.getGreen(), color.getBlue());
    }
    return true;
  }
}