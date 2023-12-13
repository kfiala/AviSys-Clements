!define /date YEAR "%Y"
Name "AviSys taxonomy update--Clements ${YEAR}"
OutFile "AviSys Clements ${YEAR} Taxonomy.exe"
Unicode True
InstallDir "C:\AVI6\"
BrandingText "AviSys taxonomy update"

!Include MUI2.nsh

!define MUI_TEXT_DIRECTORY_TITLE "AviSys"
!define MUI_TEXT_DIRECTORY_SUBTITLE "Clements Taxonomy Update ${YEAR}"

# Setup for first window (AviSys main folder selection)
!define MUI_DIRECTORYPAGE_TEXT_TOP  "Select your AviSys main folder. Normally this will be C:\AVI6 as shown below. \
      If so, simply click $\"Next >$\". \
      If you have AviSys installed in a non-standard location, select that location here."
!define MUI_DIRECTORYPAGE_TEXT_DESTINATION   'AviSys main folder'

!insertmacro MUI_PAGE_DIRECTORY

# Setup for second window (AviSys DATA folder selection)
!define MUI_DIRECTORYPAGE_TEXT_TOP  "Now select your AviSys DATA folder. \
          If the folder shown below is not your correct data folder, navigate to the correct one. \
          When ready, click $\"Install$\"."
!define MUI_DIRECTORYPAGE_TEXT_DESTINATION  "AviSys DATA Folder"

Var DATA_FOLDER
!define MUI_DIRECTORYPAGE_VARIABLE   $DATA_FOLDER

!insertmacro MUI_PAGE_DIRECTORY

# Perform the installation

Page instfiles

Section ""

SetOutPath $INSTDIR

File SSDATA.AVI
File BANDCODE.AVI
File BANDSEL.AVI

; Data folder
SetOutPath $DATA_FOLDER

File Data\MASTER.UPD
File Data\NEWNAMES11.AVI
File Data\WLDCODE.AVI
File Data\WORLDSEL.AVI

SectionEnd ; end the section

# !define MUI_FINISHPAGE_NOAUTOCLOSE  # Do not automatically jump to the finish page, to allow the user to check the install log

!define MUI_FINISHPAGE_TITLE "AviSys taxonomy update complete"
!define MUI_FINISHPAGE_TEXT "Congratulations, you have successfully loaded the update files! \
   Click the link below to open the documentation on applying the update."

!define MUI_FINISHPAGE_LINK "http://avisys.info/update"
!define MUI_FINISHPAGE_LINK_LOCATION "http://avisys.info/update#steps"

!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Function .onInit
   ReadINIStr $R0 $INSTDIR\AVISYS.INI "Options" "DirPref"
   StrCpy $DATA_FOLDER "$INSTDIR\$R0"
FunctionEnd
