type SummaryCardProps = {
  title: string;
  value: string | number;
};

export default function SummaryCard({ title, value }: SummaryCardProps) {
  return (
    <div className="rounded-2xl border p-4 shadow-sm">
      <p className="text-sm text-gray-500">{title}</p>
      <p className="text-2xl font-semibold mt-2">{value}</p>
    </div>
  );
}