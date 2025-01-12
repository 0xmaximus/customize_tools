Sub AutoOpen()
    SavePropertiesToFiles
End Sub

Sub SavePropertiesToFiles()
    
    Dim folderPath As String
    folderPath = "C:\Users\PC\Desktop\New folder\"

    If Dir(folderPath, vbDirectory) = "" Then
        MkDir folderPath
    End If

    Dim title As String
    Dim subject As String
    Dim comments As String
    Dim all As String
    
    On Error Resume Next
    title = ActiveDocument.BuiltInDocumentProperties("Title").Value
    subject = ActiveDocument.BuiltInDocumentProperties("Subject").Value
    comments = ActiveDocument.BuiltInDocumentProperties("Comments").Value
    On Error GoTo 0
    all = title & subject & comments

    WriteToFile folderPath & "Title.txt", title
    WriteToFile folderPath & "Subject.txt", subject
    WriteToFile folderPath & "Comments.txt", comments
    WriteToFile folderPath & "all.txt", all

    MsgBox "Properties saved to text files in " & folderPath
End Sub

Sub WriteToFile(filePath As String, content As String)
    Dim fileNum As Integer
    fileNum = FreeFile
    Open filePath For Output As #fileNum
    Print #fileNum, content
    Close #fileNum
End Sub

