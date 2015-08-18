package casecontrol.mode;

import java.awt.Color;

import casecontrol.Data;

public final class CaseModeStatic implements CaseMode {

  @Override
  public Color getColor() {
    return Data.caseStaticColor;
  }
}