import { LoginInput } from "../inputs";

export default function LoginForm() {
  return (
    <div className="flex flex-1 items-center justify-center">
      <div className="flex w-full max-w-[575px] flex-col gap-4">
        <LoginInput
          label="Username or Email"
          placeholder="Enter your username"
          id="username"
          type="text"
        />
        <LoginInput
          type="password"
          label="Password"
          placeholder="Enter your password"
          id="password"
        />
        <div className="pt-10">
          <button className="w-full rounded-lg bg-primary py-2 text-center font-Inter text-[26px] font-medium text-white hover:bg-opacity-95">
            Log In
          </button>
        </div>
        <p className="cursor-pointer text-center font-Inter text-lg text-raven underline">
          Forgot Password?
        </p>
      </div>
    </div>
  );
}
