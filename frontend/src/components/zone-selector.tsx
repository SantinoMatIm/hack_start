'use client';

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { MapPin } from 'lucide-react';
import type { Zone } from '@/lib/api/types';

interface ZoneSelectorProps {
  zones: Zone[];
  value: string;
  onChange: (value: string) => void;
}

export function ZoneSelector({ zones, value, onChange }: ZoneSelectorProps) {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="w-[200px]">
        <div className="flex items-center gap-2">
          <MapPin className="h-4 w-4 text-muted-foreground" />
          <SelectValue placeholder="Select zone" />
        </div>
      </SelectTrigger>
      <SelectContent>
        {zones.map((zone) => (
          <SelectItem key={zone.id} value={zone.slug}>
            {zone.name}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
