; ModuleID = 'test.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: nounwind uwtable
define i32 @fuck(i32 %x) #0 {
  %1 = alloca i32, align 4
  %y = alloca i32, align 4
  store i32 %x, i32* %1, align 4
  store i32 0, i32* %y, align 4
  %2 = load i32, i32* %1, align 4
  %3 = load i32, i32* %y, align 4
  %4 = add nsw i32 %2, %3
  ret i32 %4
}

; Function Attrs: nounwind uwtable
define i32 @main() #0 {
  %1 = alloca i32, align 4
  %a = alloca i32, align 4
  %abc = alloca i32, align 4
  %i = alloca i32, align 4
  store i32 0, i32* %1, align 4
  %2 = call i32 @fuck(i32 1)
  store i32 %2, i32* %a, align 4
  store i32 2, i32* %i, align 4
  br label %3

; <label>:3                                       ; preds = %0, %12
  %4 = load i32, i32* %abc, align 4
  %5 = load i32, i32* %i, align 4
  %6 = add nsw i32 %5, 1
  %7 = mul nsw i32 4, %6
  %8 = add nsw i32 %4, %7
  store i32 %8, i32* %abc, align 4
  %9 = load i32, i32* %abc, align 4
  %10 = icmp sgt i32 %9, 10
  br i1 %10, label %11, label %12

; <label>:11                                      ; preds = %3
  br label %13

; <label>:12                                      ; preds = %3
  br label %3

; <label>:13                                      ; preds = %11
  ret i32 0
}

attributes #0 = { nounwind uwtable "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.ident = !{!0}

!0 = !{!"clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final)"}
