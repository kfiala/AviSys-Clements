# Code for performing Clements taxonomy update for Avisys

1. Set up this directory structure:
    ```
   \work
      \scripts
      \State checklists
         \html
         \txt
      \jump tables
   \update files
      \For Data Folder
      \For Main Folder
    ```

1. Bring forward from previous year:

    | Filename | Content
    | ---      | ---
    | **bandcode.exceptions.csv** | codes to resolve collisions
    | **AOS diffs.csv**           | taxa named differently between AOS and Clements
    | **GRANDFATHER.SDT.txt**     | "Grandfathered" state checklist entries
    | **EditMaster.exe**          | AviSys program for updating taxonomy

    Also bring forward the entire contents of the **jump tables** folder.

1. Copy the current versions of scripts to the scripts folder.

1. Run `EditMaster` on the current AviSys data and select `CREATE MASTER EDIT FILE` to create **MASTER.EDT** and **STATE.SDT**. Discard **STATE.SDT**.
Move **MASTER.EDT** to the work folder and rename it as **MASTER.OLD.EDT**.

1. Download Clements checklist in CSV format to work folder.

1. Download the current ABA checklist in CSV format to work folder.

1. Check for any changes in the format of either CSV file and update **clements.py** and/or **ABA.py** accordingly.

1. Run scripts from a Powershell window with the work folder as the current directory.

1. Run `python scripts\clements.py`. Six files will be created in the work directory:

    | Filename | Contents|
    | --- | --- |
    | **changes.csv**    | contains lines from Clements that report taxonomic changes
    | **subspecies.txt** | input for creating SSDATA.AVI
    | **longnames.txt**  | names that will need to be shortened for AviSys (max 36 characters)
    | **lostnames.txt**  | names in the old taxonomy that are not in the new
    | **newnames.txt**   | names in the new taxonomy that were not in the old
    | **MASTER.EDT**     | the new taxonomy for input to EditMaster.exe

1. If the results show that there are any new names that differ between AOS (ABA) and Clements (eBird),
update **AOS diffs.csv** and run `clements.py` again.

1. Edit **MASTER.EDT** to shorten names listed in longnames.txt, if any. Examples:

    | Long name | Shortened name
    | --------- | ---
    | TIT BERRYPECKER AND CRESTED BERRYPECKER |  TIT BERRYPECKER~ CRESTED BERRYPECKER
    | VIREOS~ SHRIKE-BABBLERS~ AND ERPORNIS   |  VIREOS~ SHRIKE-BABBLERS~ ERPORNIS
    | TREE-BABBLERS~ SCIMITAR-BABBLERS~ AND ALLIES |  TREE-BABBLERS~ SCIMITAR-BABBLERS ETC

1. Obtain state lists from eBird.
    1. Run `scripts\wgetChecklists.ps1` to download state checklist web pages into **\State checklists\html** folder.
    1. Run `python scripts\statesFromHtml.py` to extract species lists from web pages and write to **\State checklists\txt** folder.
    1. Check over the state checklists for species that should be removed.

1. Species on the grandfather list are accepted by state checklist committees but records may be only historical, with none in eBird.
Update species names in **grandfather.SDT.txt** as necessary. If there are splits or lumps of any grandfathered species,
update the bit masks as necessary.
The bit mask definitions can be found in **statesToSDT.py**.

1. Run `python scripts\statesToSDT.py` to create **STATE.SDT** from state checklists and **grandfather.SDT.txt**.

1. Run `EditMaster` and choose `CREATE UPDATE MASTER CHECKLIST` to generate the new **MASTER.UPD**.

1. Run `python scripts\jerry.py subspecies.txt encode` to produce **subspecies.txt.jerry**; rename it as **SSDATA.AVI**


1. Edit **changes.csv**
   1. Remove 1-to-1 renames to new spreadsheet **NEWNAMES11.AVI.CSV**, with old name in column A and new name in column B.
       Run `python scripts\makenewnames.py` to create **NEWNAMES11.AVI**.
   1. Manually update summary of changes. **renames.html** for name changes, and **changes.html** with splits and lumps that remain in **changes.csv**.
   This is a time-consuming step and I may not do it in the future, since the Clements summary is fairly good.

1. Copy **MASTER.UPD** and **NEWNAMES11.AVI** to an AviSys data folder, and copy **SSDATA.AVI** to main folder, and run the AviSys update.

1. Run `EditMaster` in the data folder and `CREATE MASTER EDIT FILE` to get the final **MASTER.EDT** with any ABA status changes applied.
   Replace **MASTER.EDT** in the work folder with this new one.
   In the work folder, run `EditMaster` (`CREATE UPDATE MASTER CHECKLIST`) to get final **MASTER.UPD**

1. Run `python scripts\cleanmaster.py` to clean up **MASTER.UPD**. (Produces **remaster.upd**; delete **MASTER.UPD** and rename **remaster.upd** to **MASTER.UPD**).

1. Update **bandcode.exceptions.csv** as necessary

1. Run `python scripts\bandcodes.py` to create **BANDCODE.new.AVI** and **BANDSEL.new.AVI**.
   Rename these files as **BANDCODE.AVI** and **BANDSEL.AVI**.

1. Edit **BANDSEL.AVI** to put most likely species first in each list.

1. Update jump lists if necessary.
   If any changes in aliases, run `python scripts\makealias.py WORLD` to create **jump tables\Walias.avi**
   and `python scripts\makealias.py N.A.` to create **jump tables\Alias.avi**
   Beware the AviSys support for jump table aliases is buggy and it may take some trial and error to get a table that works for each alias.
   That's why I have some dummy entries.

1. Generate world codes and add these special cases to **WLDCODE.AVI**. Species marked "dup" must also be added to **WORLDSEL.AVI**.
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
1. Copy (or move) files to their destination:

    | File | Destination folder |
    | ---- | --- |
    | `MASTER.UPD`, `NEWNAMES11.AVI`, `WLDCODE.AVI`, `WORLDSEL.AVI` | `\update files\For Data Folder` |
    | `Alias.avi`, `Alpha.avi`, `BANDCODE.AVI`, `BANDSEL.AVI`, `Famfile.avi`, `SSDATA.AVI`, `Walias.avi`, `Wfam.avi`, `Wfam2.avi` | `\update files\For Main folder`|
