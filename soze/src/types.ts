export type Color = string;

export enum LedMode {
  Off = 'off',
  Static = 'static',
  Fade = 'fade',
}

export interface LedSettings {
  mode: LedMode;
  static: {
    color: Color;
  };
  fade: {
    colors: Color[];
    saved: {
      name: string;
      colors: Color[];
    };
    fade_time: number;
  };
}

export enum LcdMode {
  Off = 'off',
  Clock = 'clock',
}

export interface LcdSettings {
  mode: LcdMode;
  color: Color;
}
