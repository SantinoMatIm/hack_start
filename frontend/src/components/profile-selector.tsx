'use client';

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Building2, Landmark } from 'lucide-react';
import type { Profile } from '@/lib/api/types';

interface ProfileSelectorProps {
  value: Profile;
  onChange: (value: Profile) => void;
}

const profiles: { value: Profile; label: string; icon: typeof Building2 }[] = [
  { value: 'government', label: 'Government', icon: Landmark },
  { value: 'industry', label: 'Industry', icon: Building2 },
];

export function ProfileSelector({ value, onChange }: ProfileSelectorProps) {
  return (
    <Select value={value} onValueChange={(v) => onChange(v as Profile)}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Select profile" />
      </SelectTrigger>
      <SelectContent>
        {profiles.map((profile) => {
          const ProfileIcon = profile.icon;
          return (
            <SelectItem key={profile.value} value={profile.value}>
              <div className="flex items-center gap-2">
                <ProfileIcon className="h-4 w-4" />
                <span>{profile.label}</span>
              </div>
            </SelectItem>
          );
        })}
      </SelectContent>
    </Select>
  );
}
