/**
 * @param {Object} props
 * @param {React.ReactNode} props.children
 * @param {string} props.label
 */

export default function Input({ children, label, ...rest }) {
  return (
    <div className="grid gap-2 max-w-[calc(100%-2.25rem)]">
      <label className="text-lg" htmlFor={rest.id}>
        {label}
      </label>
      <div className="py-2 px-4 bg-gray-500 text-white rounded flex gap-1 items-center w-full ">
        <input
          className="outline-none border-none bg-transparent w-full"
          {...rest}
        />
        {children}
      </div>
    </div>
  );
}
