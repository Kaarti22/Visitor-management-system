"use client";

import * as React from "react";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { CalendarIcon } from "lucide-react";
import { format } from "date-fns";

interface DateTimePickerProps {
  label: string;
  value: Date | undefined;
  onChange: (date: Date) => void;
}

export const DateTimePicker = ({
  label,
  value,
  onChange,
}: DateTimePickerProps) => {
  const [selectedDate, setSelectedDate] = React.useState<Date | undefined>(
    value
  );
  const [selectedTime, setSelectedTime] = React.useState<string>("10:00");

  const timeSlots = Array.from({ length: 96 }, (_, i) => {
    const hour = Math.floor(i / 4);
    const minute = (i % 4) * 15;
    return `${hour.toString().padStart(2, "0")}:${minute
      .toString()
      .padStart(2, "0")}`;
  });

  // ✅ Automatically combine date + time and send via onChange
  React.useEffect(() => {
    if (selectedDate && selectedTime) {
      const [hour, minute] = selectedTime.split(":").map(Number);
      const localDate = new Date(selectedDate);
      localDate.setHours(hour, minute, 0, 0);
      onChange(new Date(localDate));
    }
  }, [selectedDate, selectedTime]);

  return (
    <Card className="bg-white dark:bg-gray-800 shadow border">
      <CardContent className="p-4 flex flex-col md:flex-row gap-4 items-stretch">
        {/* Calendar */}
        <div className="w-full md:w-2/3">
          <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
            <CalendarIcon className="h-4 w-4" /> {label}
          </h4>
          <Calendar
            mode="single"
            selected={selectedDate}
            onSelect={setSelectedDate}
            defaultMonth={selectedDate}
            showOutsideDays={false}
          />

          {/* ✅ Show selected value */}
          {selectedDate && selectedTime && (
            <p className="text-xs text-gray-500 mt-2">
              Selected:{" "}
              {format(
                new Date(
                  selectedDate.setHours(
                    Number(selectedTime.split(":")[0]),
                    Number(selectedTime.split(":")[1])
                  )
                ),
                "PPpp"
              )}
            </p>
          )}
        </div>

        {/* Time Picker */}
        <div className="w-full md:w-1/3 border-t md:border-t-0 md:border-l dark:border-gray-700 flex flex-col gap-2 max-h-72 overflow-y-auto pt-4 md:pt-0 md:pl-4">
          {timeSlots.map((time) => (
            <Button
              key={time}
              onClick={() => setSelectedTime(time)}
              variant={selectedTime === time ? "default" : "outline"}
              className="w-full text-sm cursor-pointer"
            >
              {time}
            </Button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};
