package me.lucaspickering.casecontrol;

import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.Namespace;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InvalidClassException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.Timer;
import java.util.TimerTask;

import me.lucaspickering.casecontrol.command.Command;
import me.lucaspickering.casecontrol.command.EnumCommand;
import me.lucaspickering.casecontrol.mode.caseled.CaseMode;
import me.lucaspickering.casecontrol.mode.caseled.EnumCaseMode;
import me.lucaspickering.casecontrol.mode.lcd.EnumLcdMode;
import me.lucaspickering.casecontrol.mode.lcd.LcdMode;

public final class CaseControl {

    // Argument parser
    private static final ArgumentParser ARG_PARSER =
        ArgumentParsers.newArgumentParser("Case-Control")
            .defaultHelp(true)
            .description("Control LEDs and LCD over a serial connection");
    // Argument names
    private static final String PORT_OPT = "port";

    static {
        // Create command line arguments
        ARG_PARSER.addArgument("-p", "--port")
            .required(true)
            .help("the serial port to communicate over");
    }

    private static CaseControl caseControl;
    private static boolean run = true;

    private Timer caseModeTimer;
    private Timer lcdModeTimer;
    private final SerialThread serialThread;
    private Data data = new Data();
    private final Map<String, Command> commands = new HashMap<>();

    public static void main(String[] args) {
        // Parse command line arguments
        final Namespace nameSpace;
        try {
            nameSpace = ARG_PARSER.parseArgs(args);
        } catch (ArgumentParserException e) {
            throw new RuntimeException("Error parsing arguments", e);
        }

        // Access arguments
        final String serialPortName = nameSpace.getString(PORT_OPT);

        // Init the program and start the main loop
        caseControl = new CaseControl(serialPortName);
        caseControl.inputLoop();
    }

    private CaseControl(String serialPortName) {
        serialThread = new SerialThread(serialPortName);
    }

    public static Data data() {
        return caseControl.data;
    }

    public static void stop() {
        run = false;
    }

    public static void restartCaseTimer(String... modeArgs) {
        caseControl.caseModeTimer.cancel(); // Stop the old timer
        caseControl.startCaseTimer(data(), modeArgs); // Start the new timer
    }

    public static void restartLcdTimer(String... modeArgs) {
        caseControl.lcdModeTimer.cancel(); // Stop the old timer
        caseControl.startLcdTimer(data(), modeArgs); // Start the new timer
    }

    /**
     * Constantly receives input from the user. Main loop of the program.
     */
    private void inputLoop() {
        Runtime.getRuntime().addShutdownHook(serialThread); // Tell the serial thread when we stop
        loadData(); // Load saved data (if possible)

        startCaseTimer(data); // Spawn a thread to periodically update the case data
        startLcdTimer(data); // Spawn a thread to periodically update the LCD data
        serialThread.start(); // Start the thread that communicates over the serial port

        // Register all top-level commands
        for (EnumCommand command : EnumCommand.values()) {
            commands.put(command.command.getName(), command.command);
        }
        Scanner scanner = new Scanner(System.in); // Scanner to get input from the command lin
        do {
            System.out.print(">");
            runInput(scanner.nextLine().toLowerCase());
            saveData(); // Save data after each command (it's cheap)
        } while (run);

        // Stop the timers/threads
        caseModeTimer.cancel();
        lcdModeTimer.cancel();
        serialThread.terminate();

        System.out.println("Exiting...");
    }

    /**
     * Interprets input from the user.
     *
     * @param input the input from the user, must be lower case
     */
    private void runInput(String input) {
        String[] splits = input.split(" "); // Split the input into words.
        String commandName = splits[0];
        if (commands.containsKey(commandName)) {
            Command command = commands.get(commandName);
            // Keep going down the array until the next string in there isn't a sub-command
            int i;
            for (i = 1; i < splits.length; i++) {
                if (command.isSubcommand(splits[i])) {
                    command = command.getSubcommand(splits[i]);
                } else {
                    break;
                }
            }
            // command is now the lowest-level sub-command possible. All remaining strings in splits
            // are arguments (if there are any at all).

            // Execute command with arguments
            if (!command.execute(Arrays.copyOfRange(splits, i, splits.length))) {
                if (command.hasSubcommands()) {
                    System.out.println("Available sub-commands:");
                    command.printSubcommands();
                } else {
                    Funcs.printCommandInfo(command);
                }
            }
        } else {
            System.out.println("That was not a valid command. Maybe try \'help\'.");
        }
    }

    /**
     * Starts a {@link Timer} to periodically process case data.
     *
     * @param data the current data state
     */
    private void startCaseTimer(Data data, String... modeArgs) {
        final EnumCaseMode caseModeType = data.getCaseMode();
        final CaseMode caseMode = caseModeType.instantiateMode();

        // Create a task to be called on a regular interval to update the case color
        final TimerTask task = new TimerTask() {
            @Override
            public void run() {
                data.setCaseColor(caseMode.getColor());
            }
        };
        caseModeTimer = new Timer();
        caseModeTimer.schedule(task, 0L, caseModeType.updatePeriod);
    }

    /**
     * Starts a {@link Timer} to periodically process case data.
     *
     * @param data     the current data state
     * @param modeArgs the argument(s) that should be passed into the mode on initialization
     */
    private void startLcdTimer(Data data, String... modeArgs) {
        final EnumLcdMode lcdModeType = data.getLcdMode();
        final LcdMode lcdMode = lcdModeType.instantiateMode();
        lcdMode.init(modeArgs);

        // Create a task to be called on a regular interbal to update the LCD color/text
        final TimerTask task = new TimerTask() {
            @Override
            public void run() {
                data.setLcdColor(lcdMode.getColor());
                data.setLcdText(lcdMode.getText());
            }
        };
        lcdModeTimer = new Timer();
        lcdModeTimer.schedule(task, 0L, lcdModeType.updatePeriod);
    }

    private void saveData() {
        try {
            FileOutputStream fileOut = new FileOutputStream(Consts.DATA_FILE);
            ObjectOutputStream objectOut = new ObjectOutputStream(fileOut);

            objectOut.writeObject(data());

            objectOut.close();
            fileOut.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void loadData() {
        try {
            final File file = new File(Consts.DATA_FILE);
            if (file.exists()) {
                // Open the file
                FileInputStream fileIn = new FileInputStream(file);
                ObjectInputStream objectIn = new ObjectInputStream(fileIn);

                try {
                    data = (Data) objectIn.readObject(); // Read the data in
                } catch (InvalidClassException e) {
                    System.out.println("Could not load saved data. Maybe it was an older version?");
                }

                // Close the file
                objectIn.close();
                fileIn.close();
            }
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}