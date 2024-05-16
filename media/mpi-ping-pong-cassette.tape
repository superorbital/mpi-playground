# https://github.com/charmbracelet/vhs

# Where should we write the GIF?
Output demo.gif

# Set up the terminal
Set TypingSpeed 200ms
Set Shell bash
Set FontFamily "Fira Code"
Set FontSize 24
Set Width 1920
Set Height 1080
Set Margin 40
Set MarginFill "#674EFF"
Set BorderRadius 20

# Run it...
Hide
Sleep 1s
Type "kubectl delete mpijobs.kubeflow.org mpi-ping-pong"
Enter
Sleep 1s
Type "reset && clear"
Enter
Sleep 1s

Show
Type "kubectl apply -f ./manifests/mpi-ping-pong/mpijob.yaml && timeout 15 watch -q 5 -t -n 1 kubectl get pods"
Enter
Sleep 15s
Type "kubectl logs $(kubectl get pod -l job-name=mpi-ping-pong-launcher --no-headers -o name)"
Enter
Sleep 5s

