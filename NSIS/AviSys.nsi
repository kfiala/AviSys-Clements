Name "AviSys taxonomy update--Clements 2023"
OutFile "AviSys Clements 2023 Taxonomy.exe"
Unicode True
InstallDir "C:\AVI6\"
BrandingText "AviSys taxonomy update"

!Include MUI2.nsh
!Include TextFunc.nsh

!define MUI_TEXT_DIRECTORY_TITLE "AviSys"
!define MUI_TEXT_DIRECTORY_SUBTITLE "Clements Taxonomy Update 2023"

DirText 'Select your AviSys main folder. Normally this will be C:\AVI6 as shown below. \
   If so, simply click "Next >". \
   If you have AviSys installed in a non-standard location, select that location here.' \
   'AviSys main folder'

!insertmacro MUI_PAGE_DIRECTORY

Var DATA_FOLDER_GUI_TITLE
Var DATA_FOLDER_TEXT
Var DATA_FOLDER
!define MUI_DIRECTORYPAGE_TEXT_TOP          $DATA_FOLDER_GUI_TITLE
!define MUI_DIRECTORYPAGE_TEXT_DESTINATION  $DATA_FOLDER_TEXT
!define MUI_DIRECTORYPAGE_VARIABLE          $DATA_FOLDER

Function .onInit
   StrCpy $DATA_FOLDER_GUI_TITLE 'Now select your AviSys DATA folder. \
          If the folder shown below is not your correct data folder, navigate to the correct one. \
          When ready, click "Install".'
   StrCpy $DATA_FOLDER_TEXT "AviSys DATA Folder"
FunctionEnd

Function .onVerifyInstDir
   IfFileExists $INSTDIR\AVISYS.INI +1 Done
      ${ConfigRead} $INSTDIR\AVISYS.INI "DirPref=" $R0
      StrCpy $DATA_FOLDER "$INSTDIR\$R0"
   Done:
FunctionEnd

!insertmacro MUI_PAGE_DIRECTORY


Page instfiles


Section ""
; Main folder
SetOutPath $INSTDIR

File SSDATA.AVI
File BANDCODE.AVI
File BANDSEL.AVI
File Alias.avi
File Alpha.avi
File Famfile.avi
File Walias.avi
File Wfam.avi
File Wfam2.avi

; Data folder
SetOutPath $DATA_FOLDER

File Data\MASTER.UPD
File Data\NEWNAMES11.AVI
File Data\WLDCODE.AVI
File Data\WORLDSEL.AVI


SectionEnd ; end the section

; !define MUI_FINISHPAGE_NOAUTOCLOSE

!define MUI_FINISHPAGE_TITLE "AviSys taxonomy update complete"
!define MUI_FINISHPAGE_TEXT "Congratulations, you have successfully loaded the update files! \
   Click the link below to open the documentation on applying the update."
; !define MUI_FINISHPAGE_BUTTON "This is BUTTON"
!define MUI_FINISHPAGE_LINK "http://avisys.info/update"
!define MUI_FINISHPAGE_LINK_LOCATION "http://avisys.info/update#steps"

!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"
