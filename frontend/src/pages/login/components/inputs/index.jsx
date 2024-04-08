export function LoginInput({ label, ...rest }) {
  return (
    <div className="flex w-full flex-col gap-2">
      <label
        htmlFor={rest.id}
        className="font-Inter text-2xl font-medium text-blue_charcoal"
      >
        {label}
      </label>
      <input
        {...rest}
        className="hover:border-hover_color rounded-[10px] border-2 border-solitude px-2 py-3 font-Inter outline-none placeholder:text-[14px] placeholder:leading-[14px] focus-within:border-hover_color"
      />
    </div>
  );
}
