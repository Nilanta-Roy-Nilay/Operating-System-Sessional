#include <stdio.h>

// Bubble Sort function
void bubbleSort(int bt[], int n){

for(int i=0; i<n-1; i++){
   for(int j=0; j<n-i-1; j++){
     if(bt[j] > bt[j+1]){
       int temp = bt[j];
       bt[j] = bt[j+1];
       bt[j+1] = temp;
      }
    }
  }
}

// FCFS Scheduling

void FCFS(int bt[], int n){

    int wt[n], tat[n];
    wt[0] = 0;

   //calculate waiting times
   for(int i=0; i<n; i++){
     tat[i] = wt[i] + bt[i];
   }
   //calculate turnaround times
   for(int i=0; i<n; i++){
      tat[i] = wt[i] + bt[i];
   }
   // Print results
   printf("Process\tBurst\tWaiting\tTurnaround\n");
   for(int i=0; i<n; i++){
      printf("P%d\t%d\t%d\t%d\n", i+1, bt[i], wt[i], tat[i]);
   }
 }
  
 int main(){
     int n;
     printf("Enter number of processes: ");
     scanf("%d", &n);
     
     int bt[n];
     printf("Enter burst times:\n");
     for(int i=0; i<n; i++){
         scanf("%d", &bt[i]);
    }
   
   // sort burst times using Bubble Sort
   bubbleSort(bt,n);

   // Apply FCFS Scheduling
   FCFS(bt,n);

   return 0;
}
