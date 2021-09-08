# Code for performing Clements taxonomy update for Avisys

1. Clone the repository to a work folder.

1. Open a Powershell window with the work folder as the current directory. You will run scripts from there.

1. Run `python scripts\makeEDT.py C:\AVI6\{datafolder}\MASTER.AVI` in the work folder
   (substitute the name of a valid AviSys data folder for "{datafolder}").
   This will create **MASTER.EDT** in the work folder; rename it as **MASTER.OLD.EDT**.
   It also creates **Hawaii-only.txt** which may be of interest but is not otherwise used.

1. Download Clements checklist in CSV format to the work folder. Note: I have found the provided CSV format checklist
   to have improper encoding. For better results, I download the XLSX file and create my own CSV format file.

1. Download the current ABA checklist in CSV format to the work folder.

1. Check for any changes in the format of either CSV file and update `clements.py` and/or `ABA.py` accordingly.

1. Run `python scripts\clements.py`. Six files will be created in the work directory:

    | Filename | Contents|
    | --- | --- |
    | **changes.csv**    | contains lines from Clements that report taxonomic changes
    | **longnames.txt**  | names that will need to be shortened for AviSys (max 36 characters)
    | **lostnames.txt**  | names in the old taxonomy that are not in the new
    | **MASTER.EDT**     | the new taxonomy for input to `makeUpdate.py`
    | **newnames.txt**   | names in the new taxonomy that were not in the old
    | **subspecies.txt** | input for creating SSDATA.AVI

1. If the results show that there are any new names that differ between AOS (ABA) and Clements (eBird),
update **AOS diffs.csv** and run `clements.py` again.

1. Edit **MASTER.EDT** to shorten names listed in longnames.txt, if any. Examples:

    | Long name | Shortened name
    | --------- | ---
    | SHARPBILL~ ROYAL FLYCATCHER~ AND ALLIES | SHARPBILL~ ROYAL FLYCATCHER & ALLIES
    | TIT BERRYPECKER AND CRESTED BERRYPECKER | TIT BERRYPECKER~ CRESTED BERRYPECKER
    | VIREOS~ SHRIKE-BABBLERS~ AND ERPORNIS | VIREOS~ SHRIKE-BABBLERS~ ERPORNIS
    | WOODSWALLOWS~ BELLMAGPIES~ AND ALLIES | WOODSWALLOWS~ BELLMAGPIES~ & ALLIES
    | SYLVIID WARBLERS~ PARROTBILLS~ AND ALLIES | SYLVIID WARBLERS~ PARROTBILLS~ ETC
    | TREE-BABBLERS~ SCIMITAR-BABBLERS~ AND ALLIES | TREE-BABBLERS~ SCIMITAR-BABBLERS ETC

1. Run `python scripts\makeUpdate.py` to create **MASTER.UPD**.
   For informational purposes, the file **non-ABA.txt** is also created to list non-ABA species found on state checklists.
   Check to make sure that none of the "non-ABA" species are listed because of a name change. If there are such names, correct checklists and rerun `makeUpdate`.

1. Run `python scripts\jerry.py subspecies.txt encode` to produce **subspecies.txt.jerry**; rename it as **SSDATA.AVI**

1. Edit **changes.csv**
   1. Sort on column "Clements change".
   Cut the lines with "name change - English name" and paste them into a new spreadsheet.
   In the new spreadsheet, delete all the columns except "text for website" and "English name".
   Edit each "text for website" value and delete everything except for the old English name,
   so that you end up with just two columns, old names in column A and new names in column B.
   Save the new spreadsheet as **NEWNAMES11.AVI.CSV**.

   1. Delete all remaining lines from **changes.csv** except for those where the "Clements change" mentions "lump" or "split", or other species changes such as "new species", "species deletion", "reassign subspecies", etc., and save **changes.csv** for later.

   1. Run `python scripts\makenewnames.py` to create **NEWNAMES11.AVI** from **NEWNAMES11.AVI.CSV**.

1. Copy MASTER.UPD and NEWNAMES11.AVI to the data folder, and SSDATA.AVI to the main folder, and run the update. **Resolve any conflicts** and rerun as necessary.

   Then run `python scripts\makeEDT.py C:\AVI6\{datafolder}\MASTER.AVI` in the work folder again to get the final version of
   **MASTER.EDT**. This version will have any changes in N.A. status applied, needed for bandcode generation.

1. Update **bandcode.exceptions.csv** as necessary

1. Run `python scripts\bandcodes.py` to create **BANDCODE.new.AVI** and **BANDSEL.new.AVI**.
   Compare new with old to check for new conflicts. If there are any, update **bandcode.exceptions.csv** and run `bandcodes.py` again.
   Rename the new files as **BANDCODE.AVI** and **BANDSEL.AVI**.

1. Edit **BANDSEL.AVI** to sort each list with most likely species first.

1. Update jump lists if necessary.
   If any changes in aliases, run `python scripts\makealias.py WORLD` to create **jump tables\Walias.avi**
   and `python scripts\makealias.py N.A.` to create **jump tables\Alias.avi**.
   Beware the AviSys support for jump table aliases is buggy and it may take some trial and error to get a table that works for each alias.
   That's why I have some dummy entries.

1. Generate world codes and append these special cases to **WLDCODE.AVI**, then sort the file. Species marked "dup" must also be added to **WORLDSEL.AVI**, along with their duplicates.
(Also check for any new duplicates).
    ```
    daba d'arnaud's barbet     dup
    doct d'orbigny's chat-tyrant
    bobe böhm's bee-eater
    bofl böhm's flycatcher
    fubo fülleborn's boubou
    fulo fülleborn's longclaw
    lubu lühder's bushshrike   dup
    rubu rüppell's bustard     dup
    ruch rüppell's chat        dup
    rugr rüppell's griffon     dup
    rupa rüppell's parrot
    rurc rüppell's robin-chat
    rust rüppell's starling
    ruwa rüppell's warbler
    ruwe rüppell's weaver      dup
    ```

1. Copy (or move) these files to folder NSIS:
   ```
   `Alias.avi`
   `Alpha.avi`
   `BANDCODE.AVI`
   `BANDSEL.AVI`
   `Famfile.avi`
   `SSDATA.AVI`
   `Walias.avi`
   `Wfam.avi`
   `Wfam2.avi`
   ```

1. Copy (or move) these files to folder NSIS\DATA:
   ```
   `MASTER.UPD`
   `NEWNAMES11.AVI`
   `WLDCODE.AVI`
   `WORLDSEL.AVI`
   ```

1. Package the **update files** folder for distribution via NSIS.

1. Documentation: Edit **changes.csv** again, and also **NEWNAMES11.AVI.CSV**.
   1. **NEWNAMES11.AVI.CSV**: Tabulate name changes in **renames.html**.

   2. **changes.csv**: Tabulate splits and lumps in **changes.html**.
   This is a time-consuming step and I am no longer doing it as of 2019, since the information is all available in the Clements summary anyway.

1. Run the entire update to test it.
